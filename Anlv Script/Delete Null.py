# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Delete Null Objects
Name-ZH:删除空对象
Description-US:Delete Null objects that do not contain child elements in the scene.
Description-ZH:删除场景中不包含子级的空对象.
"""

import c4d

def collect_empty_objects(obj, obj_list):
    # 如果对象为空，则返回
    if obj is None:
        return

    # 检查对象是否是空对象（Null对象）且没有子对象
    if obj.CheckType(c4d.Onull) and not obj.GetDown():
        # 将空对象添加到列表中
        obj_list.append(obj)

    # 递归检查子对象
    if obj.GetDown():
        collect_empty_objects(obj.GetDown(), obj_list)
    if obj.GetNext():
        collect_empty_objects(obj.GetNext(), obj_list)

def main():
    # 获取活动文档
    doc = c4d.documents.GetActiveDocument()
    obj_list = []  # 存储空对象的列表
    collect_empty_objects(doc.GetFirstObject(), obj_list)

    # 删除收集到的空对象
    if obj_list:
        doc.StartUndo()  # 开始记录删除操作的撤销步骤
        for obj in obj_list:
            doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
            obj.Remove()
        doc.EndUndo()  # 结束记录撤销步骤

    c4d.EventAdd()

# 执行主函数main()
if __name__ == '__main__':
    main()