# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:CNV Conversion Subdivision
Name-ZH:CNV 细分对象转换器
Description-US:Convert all subdivided surface objects to Octane Object tag and add subdivision.
Description-ZH:将「细分对象」转换为「Octane 对象标签」并开启细分。（细分等级根据细分对象嵌套数设置，如未选中对象，则对整个场景进行转换。）
"""

import c4d
from c4d import gui

def get_subdivision_level(obj: c4d.BaseObject) -> int:
    '''Calculate the subdivision level of an object based on nested hierarchy, considering all Subdivision Surface parents.'''
    level = 0
    parent = obj.GetUp()
    while parent:
        if parent.GetType() == 1007455:  # ID for Subdivision Surface
            level += 2
        parent = parent.GetUp()
    return level

def get_bottommost_child(obj: c4d.BaseObject) -> c4d.BaseObject:
    '''Get the bottom-most child of an object.'''
    while obj.GetDown():
        obj = obj.GetDown()
    return obj

def recursive_collect_objects(obj, collected_objects, process_siblings=True):
    '''Recursively collect all objects in the scene and store their subdivision levels.'''
    while obj:
        level = get_subdivision_level(obj)
        collected_objects[obj] = level
        if obj.GetDown():
            recursive_collect_objects(obj.GetDown(), collected_objects, process_siblings=False)
        if not process_siblings:
            break
        obj = obj.GetNext()


def main() -> None:
    doc.StartUndo()  # Start recording undos

    # Step 1: Collect objects and their subdivision levels recursively based on selection
    all_objects = {}
    selection = doc.GetActiveObjects(0)  # Get selected objects
    if not selection:  # If no objects are selected, process all objects in the scene
        recursive_collect_objects(doc.GetFirstObject(), all_objects)
    else:  # If some objects are selected, only process those
        for obj in selection:
            recursive_collect_objects(obj, all_objects, process_siblings=False)


    subdivision_objects = [obj for obj, level in all_objects.items() if obj.GetType() == 1007455]

    # Step 2: Process each subdivision surface object's children
    for obj in subdivision_objects:
        # Get the bottom-most child (polygon object)
        bottom_child = get_bottommost_child(obj)

        # Retrieve stored subdivision level for the bottom-most child
        level = all_objects[bottom_child]

        # Add Octane object tag and set subdivision level to the polygon child
        octane_tag = bottom_child.GetTag(1029603)  # Try to get existing Octane Object Tag
        if not octane_tag:
            octane_tag = bottom_child.MakeTag(1029603)  # If not present, create a new one
            doc.AddUndo(c4d.UNDOTYPE_NEW, octane_tag)  # Add undo for new tag
        if octane_tag:
            octane_tag[c4d.OBJECTTAG_SUBDIV_LEVEL] = level  # Set the subdivision level

        # Release children (polygon objects) from the subdivision object
        child = obj.GetDown()  # Get the first child
        while child:
            # Store the global matrix of the child before removing it from the parent
            global_matrix = child.GetMg()

            doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)  # Add undo for child
            next_child = child.GetNext()
            child.InsertAfter(obj)  # Release child to the same level as subdivision object

            # Reapply the global matrix to the child after it's been removed from the parent
            child.SetMg(global_matrix)

            child = next_child

    # Step 3: Remove all collected subdivision surface objects
    for obj in subdivision_objects:
        doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)  # Add undo for subdivision object
        obj.Remove()

    doc.EndUndo()  # End recording undos
    c4d.EventAdd()  # Refresh Cinema 4D

# Execute main()
if __name__ == '__main__':
    main()




"""
####################################################
# STET 1
# 2023-01-10 新增 自动选择细分曲面对象，汉化群网友 Terry 提供
####################################################

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def getObjectsFilter(typeList):
    def isObj(o):
        for i, ty in enumerate(typeList):
            if o.GetType() == ty:
                return i
        return -1

    def getChildren(o, reList):
        children = o.GetChildren()
        if children:
            for i in children:
                if isObj(i) > -1: reList.append(i)
                getChildren(i, reList)

    result = []
    for obj in doc.GetObjects():
        if isObj(obj) > -1: result.append(obj)
        getChildren(obj, result)
    return result


def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    objList = getObjectsFilter([1007455])
    doc.SetActiveObject(objList[0], c4d.SELECTION_NEW)
    for obj in objList:
        doc.SetActiveObject(obj, c4d.SELECTION_ADD)
    c4d.EventAdd()


#
# def state():
#     # Defines the state of the command in a menu. Similar to CommandData.GetState.
#     return c4d.CMD_ENABLED
#

if __name__ == '__main__':
    main()

####################################################
#
# STET 2
#
# 选择对象的子级
#
####################################################

# Libraries
import c4d
from c4d import gui

# Global variables
hierarchy = {} # Initialize hierarchy dictionary
level = 0 # Initialize level variable (how deep object is in hierarchy)

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def GetNextObject(op): # Get next object from Object Manager
    global level # Access to global variable (level)
    if op is None: # If there is no object
        return None # Return none
    if op.GetDown(): # If can go deeper in hierarchy
        level += 1 # Going deeper in levels
        return op.GetDown() # Return object
    while not op.GetNext() and op.GetUp(): # If can't go to next object, but can go up
        level -= 1 # Going up in levels
        op = op.GetUp() # Object is parent object
    return op.GetNext() # Return object

def BuildHierarchyPath(obj): # Build hierarchy path for object
    global level # Access to global variable (level)
    path = [] # Initialize empty list for path
    for i in range(0,level+1): # Iterate through levels
        path.append(obj) # Add object to path list
        if obj.GetUp() is not None: # If can go up in Object Manager
            obj = obj.GetUp() # Going up
    path.reverse() # Reverse path list
    return path # Return hierarchy path

def BuildHierarchy(): # Build hierarchy dictionary
    global level # Access to global variable (level)
    global hierarchy # Access to global dictionary (hierarchy)
    doc = c4d.documents.GetActiveDocument()
    op = doc.GetFirstObject()
    #hierarchy = {} # Initialize empty dictionary
    i = 0 # Iteration variable
    if op is None: # If there is no object
        return # Return nothing
    while op: # While there is object
        hierarchy[i]={ # Add object information to hierarchy dictionary
            'object': op, # Object
            'level': level, # Object's level (how deep object is in Object Manager)
            'name': op.GetName(), # Object's name
            'root': FindRoot(op), # Object's root
            'path': BuildHierarchyPath(op) # Object's full path in hierarchy
        }
        op = GetNextObject(op) # Get next object from Object Manager
        i += 1 # Increase iteration variable
    return hierarchy # Return hierarchy dictionary

def FindRoot(data): # Find object's root
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        collection = [] # Initialize empty list for root object(s)
        for obj in lst: # Loop through objects in
            while obj: # Infinite loop
                if obj.GetUp() == None: # If can't go up in hierarchy
                    collection.append(obj) # Add object to collection list
                    break # Break the loop
                obj = obj.GetUp() # Go up
        return collection # Return collection of root object(s)
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        while obj: # Infinite loop
            if obj.GetUp() == None: # If can't go up in Object Manager
                return obj # Return object
                break # Break the loop
            obj = obj.GetUp() # Get up

def FindChildren(start, targetLevel=0, addRest=False): # Find children of the object
    global level # Access to global variable (level)
    global hierarchy # Access to global dictionary (hierarchy)
    collection = [] # Initialize empty list for children
    for h in hierarchy: # Loop through hierarchy
        if start == hierarchy[h]['object']: # Starting position in hierarchy
            l = hierarchy[h]['level'] # Starting level
    for counter, item in hierarchy.items(): # Loop through items in hierarchy dictionary
        for p in item['path']: # Loop through objects' paths
            if p == start: # Starting position in hierarchy
                for c, i in enumerate(item['path']): # Loop through object's path
                    if c > l: # If child of the selected object
                        if targetLevel != 0: # If there is custom target level
                            if addRest:
                                #print(addRest, l+targetLevel)
                                if c >= l + targetLevel: # If level match
                                    collection.append(i) # Add object to collection
                            else:
                                #print(addRest, l+targetLevel)
                                if c == l + targetLevel: # If level match
                                    collection.append(i) # Add object to collection
                        else: # If there is no target level (default)
                            collection.append(i) # Add object to collection
    return collection # Return collection of children

def Select(data): # Select object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Loop through list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager

def Deselect(data): # Deselect object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Data is list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    global hierarchy # Access to global dictionary (hierarchy)
    hierarchy = BuildHierarchy()
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        for obj in selection: # Loop through selection
            Deselect(obj) # Deselect selected object
            Select(FindChildren(obj, 0, True)) # Select chldren object(s)
    elif keyMod == "Shift":
        for obj in selection: # Loop through selection
            Select(FindChildren(obj, 0, True))
    elif keyMod == "Ctrl":
        inp = int(gui.InputDialog('Child level', "2"))
        for obj in selection: # Loop through selection
            Deselect(obj) # Deselect selected object
            Select(FindChildren(obj, inp, True))
    elif keyMod == "Ctrl+Shift":
        inp = int(gui.InputDialog('Child level', "2"))
        for obj in selection: # Loop through selection
            Select(FindChildren(obj, inp, True))
    elif keyMod == "Alt":
        inp = int(gui.InputDialog('Child level', "2"))
        for obj in selection: # Loop through selection
            Select(FindChildren(obj, inp, False))
    elif keyMod == "Alt+Shift":
        inp = int(gui.InputDialog('Child level', "2"))
        for obj in selection: # Loop through selection
            Select(FindChildren(obj, inp, False))

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()

####################################################
#        删除选中对象的OC对象标签(如果有)
####################################################
import c4d

def deleteTagByType(tag_type):
    # 获取活动文档和选中的对象
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    # 遍历每个选中的对象
    for obj in selected_objects:
        # 获取对象的所有标签
        tags = obj.GetTags()
        # 遍历每个标签并检查类型
        for tag in tags:
            if tag.GetType() == tag_type:
                # 如果标签类型匹配指定的ID，则删除该标签
                doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)
                tag.Remove()

    # 更新Cinema 4D界面
    c4d.EventAdd()

def main():
    # 指定要删除的标签ID
    tag_id_to_delete = 1029603
    deleteTagByType(tag_id_to_delete)

if __name__ == '__main__':
    main()

####################################################
#        添加 Octane 对象标签
####################################################

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
selection = doc.GetActiveObjects

def main() -> None:

        for i in selection(c4d.GETACTIVEOBJECTFLAGS_CHILDREN): # 循环选择对象

                OctaneObjTag = i.GetTag(1029603) #设置 tagP变量为 i.GetTag(102963)

                if OctaneObjTag is None:#如果 tagP 为空
                    i.InsertTag(c4d.BaseTag(1029603))# 为i插入OC对象标签
                    Tag = i.GetTag(1029603)
                    Tag()[c4d.OBJECTTAG_SUBDIV_LEVEL] = 1
                    Tag()[c4d.ID_BASELIST_NAME] = "Octane 细分曲面"

                else:
                    i.KillTag(1029603)    #反之若对象存在则删除oc对象标签

        c4d.EventAdd() # 刷新

if __name__ == '__main__':
    main()

####################################################
#       选择对象的父级
####################################################

# Libraries
import c4d

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def Select(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetUp(op, safe):
    pred = op # Store old object
    op = op.GetUp() # Get parent object
    if op == None: # If object is none
        if safe: # If safe mode is enabled
            return pred # Return old object
        return None # Return none
    else: # Otherwise
        return op # Return the object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        for s in selection: # Loop through selection
            Deselect(s) # Deselect original object
            Select(GetUp(s, True)) # Select parent object
    elif keyMod == "Shift":
        for s in selection:
            Select(GetUp(s, True))
    elif keyMod == "Ctrl":
        for s in selection:
            Deselect(s) # Deselect original object
            Select(GetUp(s, False))
    elif keyMod == "Ctrl+Shift":
        for s in selection:
            Select(GetUp(s, False))

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()

####################################################
#       删除对象(不包含子级)
####################################################

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument # The active document
op: Optional[c4d.BaseObject] # The active object, None if unselected

def main() -> None:

    c4d.CallCommand(1019951) # 删除(不包含子级)


if __name__ == '__main__':
    main()
    c4d.EventAdd()
"""