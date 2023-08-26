# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Del Protection Tag
Name-ZH:删除保护标签
Description-US:Remove All Protection Tag In The Scene.
Description-ZH:删除场景中所有的保护标签
"""

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument # The active document
op: Optional[c4d.BaseObject] # The active object, None if unselected

def main() -> None:

    c4d.CallCommand(100004766) # Select All

if __name__ == '__main__':
    main()
    c4d.EventAdd()

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
            if tag.CheckType(c4d.Tbase) and tag.GetName() == "Protection":
                # 如果标签类型匹配指定的类型并且名称为"Protection"，则删除该标签
                doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)
                tag.Remove()

    # 更新Cinema 4D界面
    c4d.EventAdd()

def main():
    # 指定要删除的标签类型
    tag_type_to_delete = c4d.Tbase
    deleteTagByType(tag_type_to_delete)

if __name__ == '__main__':
    main()


from typing import Optional
import c4d

doc: c4d.documents.BaseDocument # The active document
op: Optional[c4d.BaseObject] # The active object, None if unselected

def main() -> None:

    c4d.CallCommand(100004794) # Invert Selection


if __name__ == '__main__':
    main()
    c4d.EventAdd()