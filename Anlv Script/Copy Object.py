# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Copy Object
Name-ZH:复制对象
Description-US:Copy the currently selected object.
Description-ZH:拷贝一份当前选中的对象.
"""

import c4d

def main():
    # 获取当前文档和选择的对象
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    if len(selected_objects) == 0:
        return

    # 获取选中对象的父级对象
    parent_obj = selected_objects[0].GetUp()

    # 复制选中的对象并将其添加到选中对象的下方
    for obj in selected_objects:
        copied_obj = obj.GetClone()
        doc.InsertObject(copied_obj, parent_obj, obj)

    # 更新场景
    c4d.EventAdd()

    # 激活选中的对象
    doc.SetActiveObject(selected_objects[0], c4d.SELECTION_NEW)

if __name__=='__main__':
    main()