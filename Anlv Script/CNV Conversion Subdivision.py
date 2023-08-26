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

