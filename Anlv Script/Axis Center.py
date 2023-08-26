# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Axis Center
Name-ZH:轴心控制
Description-US: The selected object is centered on the axis. (SHIFT-CLICK: The axis of the selected object is placed at the bottom)
Description-ZH: 选中的对象轴心居中。（SHIFT-CLICK：选中的对象轴心置于底部）
"""

# 2023/08/18 对齐底部前先将坐标轴方向对齐世界坐标
import c4d
from c4d.modules import snap

# Functions
def AxisToOrigin(obj):
    """ Puts object's axis to the world origin """
    if obj.CheckType(c4d.Opoint): # If point object
        matOld = obj.GetMg() # Store object's original matrix
        workplane = snap.GetWorkplaneObject(doc) # Get workplane
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Record undo for changing object
        obj.SetMg(workplane.GetMg()) # Set object's matrix

        if obj.CheckType(c4d.Opoint): # If point object
            mat  = obj.GetMg() # Get global matrix
            cnt  = obj.GetPointCount() # Get point count
            
            # WIP (Normal tag handling)
            #nt   = None
            #tags = obj.GetTags() # Get object's tags
            #for t in tags: # Iterate through tags
            #    if t.CheckType(c4d.Tnormal): # If normal tag
            #        nt = t # Store normal tag

            for i in range(cnt): # Iterate through points
                pos = obj.GetPoint(i) # Get point position
                posGlobal = matOld * pos # Calculate global point position
                obj.SetPoint(i, ~mat * posGlobal) # Set new point position

                # Fix tangents
                if (obj.CheckType(c4d.Ospline) and obj[c4d.SPLINEOBJECT_TYPE] == c4d.SPLINEOBJECT_TYPE_BEZIER): # If spline object and bezier type
                        posNew = obj.GetPoint(i) # Get new position
                        tan = obj.GetTangent(i) # Get tangent
                        tan_l = tan['vl'] + pos # Left tangent
                        tan_r = tan['vr'] + pos # Right tangent
                        tan_l_glo = matOld * tan_l
                        tan_r_glo = matOld * tan_r
                        tan_l_new = ~mat * tan_l_glo - posNew
                        tan_r_new = ~mat * tan_r_glo - posNew
                        obj.SetTangent(i, tan_l_new, tan_r_new) # Set new tangent

        obj.Message(c4d.MSG_UPDATE)
    else: # Otherwise
        print("Select editable object!")
    return True # All good!

def main():
    doc = c4d.documents.GetActiveDocument()
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    # Check if Shift key is pressed
    input_state = c4d.BaseContainer()
    c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_SHIFT, input_state)
    shift_pressed = input_state[c4d.BFM_INPUT_VALUE]

    for obj in selection:
        if shift_pressed:
            AxisToOrigin(obj) # Execute script 1

        if obj.CheckType(c4d.Opolygon): # 检查对象是否为多边形对象
            ps = obj.GetAllPoints() # 获取对象的所有顶点坐标
            m = obj.GetMg() # 获取对象的全局矩阵

            center = obj.GetMp() # 获取对象的局部坐标中心点
            rad = obj.GetRad() # 获取对象的几何半径

            if shift_pressed:
                center -= c4d.Vector(0,rad.y,0) # 将中心点沿y轴向下移动到最低点，如果不需要移动，可以注释掉这一行

            center *= m # 将中心点转换为全局坐标

            new_m = c4d.Matrix(m) # 复制矩阵
            new_m.off = center # 修改矩阵的中心点

            loc_m = ~new_m * m # 获取局部矩阵

            obj.SetAllPoints([loc_m.Mul(p) for p in ps]) # 将所有顶点坐标乘以局部矩阵，实现局部坐标系的变换
            obj.SetMg(new_m) # 设置对象的全局矩阵为新的矩阵

            obj.Message(c4d.MSG_UPDATE) # 发送更新消息

    c4d.EventAdd()

if __name__ == '__main__':
    main()
    
