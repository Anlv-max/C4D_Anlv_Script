#Use at your own risk
"""
Name-US:Add MoGraph Cache Tag
Name-ZH:添加运动图形缓存标签
Description-US:Add MoGraph Cache Tag To All Motion Graphic Objects In The Scene.
Description-ZH:为场景中的所有运动图形对象添加运动图形缓存标签.
"""

from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # 活动文档
op: Optional[c4d.BaseObject]  # 活动对象，如果未选中则为None

def getMotionGraphicObjects():
    # 运动图形对象的类型ID列表
    motion_graphic_ids = [1018544, 1018545, 1036557, 1018791, 1018655, 1018957, 440000054]

    def isMotionGraphicObj(o):
        return o.GetType() in motion_graphic_ids

    def getChildren(o, reList):
        # 递归获取对象的子对象并加入结果列表
        children = o.GetChildren()
        if children:
            for i in children:
                if isMotionGraphicObj(i):
                    reList.append(i)
                getChildren(i, reList)

    result = []
    for obj in doc.GetObjects():
        if isMotionGraphicObj(obj):
            result.append(obj)
        getChildren(obj, result)
    return result

def main() -> None:
    # 当用户选择插件时调用。类似于CommandData.Execute。
    objList = getMotionGraphicObjects()
    if objList:
        doc.SetActiveObject(objList[0], c4d.SELECTION_NEW)
        for obj in objList[1:]:
            doc.SetActiveObject(obj, c4d.SELECTION_ADD)
        c4d.EventAdd()

if __name__ == '__main__':
    main()

# 删除选中对象的运动图形缓存标签

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
    tag_id_to_delete = 1019337
    deleteTagByType(tag_id_to_delete)

if __name__ == '__main__':
    main()


# 添加运动图形缓存标签
import c4d

def addTagAndActivate(tag_id):
    # 获取活动文档和选中的对象
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    added_tags = []  # 存储新添加的标签的列表

    # 遍历每个选中的对象
    for obj in selected_objects:
        # 创建具有指定ID的新标签
        new_tag = c4d.BaseTag(tag_id)
        # 将新标签添加到对象
        obj.InsertTag(new_tag)
        # 将新创建的标签添加到列表中
        added_tags.append(new_tag)

    # 将所有具有指定ID的标签设置为活动状态
    for tag in added_tags:
        doc.SetActiveTag(tag, c4d.SELECTION_ADD)

    # 更新Cinema 4D界面
    c4d.EventAdd()

def main():
    # 指定要添加和激活的标签ID
    tag_id_to_add = 1019337
    addTagAndActivate(tag_id_to_add)

if __name__ == '__main__':
    main()