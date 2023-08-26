# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Act on same TAG-Types
Name-ZH:选择相同标签
Description-US:Click the button after selecting a tag, and select tags of the same type.
Description-ZH:选中一个标签后点击左键，将选中相同类型的标签。
"""

import c4d

def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def ActivateTags(op, tag):
    if op is None:
        return
    while op:
        tags = op.GetTags()
        for t in tags:
            if t.GetType() == tag.GetType():
                t.SetBit(c4d.BIT_ACTIVE)
        op = GetNextObject(op)

def main():
    doc = c4d.documents.GetActiveDocument()
    selection = doc.GetSelection()
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    selectedTags = []
    start_object = doc.GetFirstObject()

    if activeObjects:
        sel = True
    elif not activeObjects:
        sel = False

    for s in selection:
        if isinstance(s, c4d.BaseTag):
            selectedTags.append(s)

    for tag in selectedTags:
        ActivateTags(start_object, tag)

    c4d.EventAdd()

if __name__ == '__main__':
    main()