# https://www.behance.net/anlv
# Works With Cinema 4D 2026
# USE AT YOUR OWN RISK

"""
Name-US:Asix Center
Name-CN:轴心居中
Description-US:[ Default ] Center axis for Object & Children.<br>[ SHIFT ] Center axis for Object only.<br>[ CTRL ] Center axis for Children only.<br>[ ALT ] Center axis for Selected Points/Polygons.<br>[ CTRL+ALT ] Center axis to Bottom (Min Y).
Description-CN:[ 默认 ] 轴心对齐到【对象及其子级】中心。<br>[ SHIFT ] 仅对齐【对象自身】中心。<br>[ CTRL ] 仅对齐【所有子级】中心。<br>[ ALT ] 对齐到【选中点/面】中心。<br>[ CTRL+ALT ] 对齐到【对象/层级】底部。

Change log:
2026/02/28 1.0.0 - 修复生成器（如挤压）轴心偏移问题，不再计算Cache，回归子对象几何中心逻辑；修复样条对象组件模式报错；重构递归逻辑以支持层级轴心处理。
2026/02/28 1.1.0 - 修改 CTRL+ALT 逻辑：仅移动所选对象轴心至整体底部 (包含子级包围盒)，不再递归重置子级轴心。
"""

import c4d

def GetInputQualifiers():
    """检测当前按下的修饰键"""
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_QUALIFIER, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        return qualifier
    return 0

def GetObjectPointsGlobal(obj):
    """获取对象所有点的世界坐标列表"""
    if not isinstance(obj, c4d.PointObject):
        return []
    mg = obj.GetMg()
    return [mg * p for p in obj.GetAllPoints()]

def GetSelectionPointsGlobal(obj):
    """获取对象选中元素（点/面）的中心点列表（世界坐标）"""
    if not isinstance(obj, c4d.PointObject):
        return []

    mg = obj.GetMg()
    all_points = obj.GetAllPoints()
    cnt = len(all_points)
    if cnt == 0: return []

    bs_point = obj.GetPointS()
    bs_poly = obj.GetPolygonS() if isinstance(obj, c4d.PolygonObject) else None

    selected_indices = []

    doc = obj.GetDocument()
    mode = doc.GetMode()

    if mode == c4d.Mpoints:
        if bs_point.GetCount() > 0:
            selected_indices = [i for i, sel in enumerate(bs_point.GetAll(cnt)) if sel]

    elif mode == c4d.Mpolygons:
        if bs_poly and bs_poly.GetCount() > 0:
            poly_count = obj.GetPolygonCount()
            poly_sel = bs_poly.GetAll(poly_count)
            temp_indices = set()
            for i, sel in enumerate(poly_sel):
                if sel:
                    poly = obj.GetPolygon(i)
                    temp_indices.add(poly.a)
                    temp_indices.add(poly.b)
                    temp_indices.add(poly.c)
                    if poly.c != poly.d:
                        temp_indices.add(poly.d)
            selected_indices = list(temp_indices)

    elif mode == c4d.Medges:
        # 边模式暂未完全支持，回退到检查是否有任何点被隐式选中
        pass

    # 回退搜索（若当前模式无选择）
    if not selected_indices:
        if bs_point.GetCount() > 0:
             selected_indices = [i for i, sel in enumerate(bs_point.GetAll(cnt)) if sel]
        elif bs_poly and bs_poly.GetCount() > 0:
            poly_count = obj.GetPolygonCount()
            poly_sel = bs_poly.GetAll(poly_count)
            temp_indices = set()
            for i, sel in enumerate(poly_sel):
                if sel:
                    poly = obj.GetPolygon(i)
                    temp_indices.add(poly.a)
                    temp_indices.add(poly.b)
                    temp_indices.add(poly.c)
                    if poly.c != poly.d:
                        temp_indices.add(poly.d)
            selected_indices = list(temp_indices)

    if selected_indices:
        return [mg * all_points[i] for i in selected_indices]
    return []

def CollectPointsRecursive(obj, include_self=True, include_children=True):
    """递归收集点坐标 (备用算法，主要用于特殊情况)"""
    if obj.GetEditorMode() == c4d.MODE_OFF:
        return []

    points = []

    # 收集自身
    has_children = obj.GetDown() is not None

    if include_self:
        if isinstance(obj, c4d.PointObject):
            points.extend(GetObjectPointsGlobal(obj))
        elif not has_children or not include_children:
            # 没有子级，或者是强制只看自身（虽然生成器自身没点，但此时看 Cache 是合理的）
            cache = obj.GetDeformCache() or obj.GetCache()
            if cache:
                points.extend(CollectPointsRecursive(cache, True, True))

    # 收集子级
    if include_children:
        for child in obj.GetChildren():
            points.extend(CollectPointsRecursive(child, True, True))

    return points

def CalculateCenter(points, align_bottom=False):
    """
    计算点集的包围盒中心 (Ver 2.5 优化版)
    :param align_bottom: 如果为 True，Y 轴将对齐到包围盒底部 (Min Y)
    """
    if not points:
        return None

    # 使用 min/max 函数直接处理列表，比手动循环快
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z for p in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    center_y = (min_y + max_y) * 0.5
    if align_bottom:
        center_y = min_y

    return c4d.Vector((min_x + max_x) * 0.5,
                      center_y,
                      (min_z + max_z) * 0.5)

def SetAxisCenter(doc, obj, center_pos):
    """
    将对象 obj 的轴心移动到 center_pos (世界坐标)。
    保持几何体和子对象在世界空间不动。
    """
    if center_pos is None:
        return

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

    # 1. 记录当前状态
    old_mg = obj.GetMg()

    # 记录直接子级的全局矩阵，以便稍后恢复它们的位置
    children = obj.GetChildren()
    children_mgs = [child.GetMg() for child in children]
    for child in children:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)

    # 2. 设置新的全局矩阵（仅位置改变，旋转缩放不变）
    new_mg = c4d.Matrix(old_mg)
    new_mg.off = center_pos
    obj.SetMg(new_mg)

    # 3. 修正几何体点的位置 (如果是点对象)
    if isinstance(obj, c4d.PointObject):
        points = obj.GetAllPoints()
        new_mg_inv = ~new_mg
        new_local_points = [new_mg_inv * (old_mg * p) for p in points]

        obj.SetAllPoints(new_local_points)
        obj.Message(c4d.MSG_UPDATE)

    # 4. 恢复子对象的世界位置
    for i, child in enumerate(children):
        child.SetMg(children_mgs[i])

def CollectChildrenMps(obj, mp_list, include_rad=False):
    """递归收集子级对象的 GetMp 点 (Ver 2.8 最终修正版: 恢复Mp模式)"""
    zero_vec = c4d.Vector(0)

    def _collect(curr_obj):
        child = curr_obj.GetDown()
        while child:
            if child[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == c4d.MODE_OFF:
                child = child.GetNext()
                continue

            is_point_obj = isinstance(child, c4d.PointObject)

            if is_point_obj or child.GetRad() != zero_vec:
                mg = child.GetMg()
                mp = child.GetMp()

                # 策略修正：
                # 只有当 include_rad 为 True (底部对齐模式) 时，才收集包围盒8角点。
                # 在默认/中心对齐模式下，MagicCenter 仅使用子对象的 Mp (几何中心) 进行平均，
                # 而不考虑子对象的包围盒大小。这对 Null 组和生成器尤为重要。

                if include_rad:
                    rad = child.GetRad()
                    rx, ry, rz = rad.x, rad.y, rad.z
                    mx, my, mz = mp.x, mp.y, mp.z

                    mp_list.extend([
                        mg * c4d.Vector(mx-rx, my-ry, mz-rz),
                        mg * c4d.Vector(mx+rx, my-ry, mz-rz),
                        mg * c4d.Vector(mx-rx, my+ry, mz-rz),
                        mg * c4d.Vector(mx+rx, my+ry, mz-rz),
                        mg * c4d.Vector(mx-rx, my-ry, mz+rz),
                        mg * c4d.Vector(mx+rx, my-ry, mz+rz),
                        mg * c4d.Vector(mx-rx, my+ry, mz+rz),
                        mg * c4d.Vector(mx+rx, my+ry, mz+rz)
                    ])
                else:
                    mp_list.append(mg * mp)

            _collect(child)
            child = child.GetNext()

    _collect(obj)

# (已移除未使用的 Cache 相关函数)

def GetObjectCenter(obj, include_children=False, align_bottom=False):
    """
    智能获取对象中心 (Ver 2.9 混合策略版)
    - 策略核心：解决生成器(包围盒)与普通层级(Mp平均)的计算差异
    - 多边形/样条: 优先使用 Mp (几何中心)
    - 生成器/组:
        - 如果是底部对齐 (Min Y)，强制使用 Recursive BBox (include_rad=True)
        - 如果是中心对齐:
            - MagicCenter 对生成器(如细分/挤压)似乎倾向于使用 BBox 中心
            - 但对普通 Null 组倾向于使用 Mp 平均
    """
    points_to_calc = []

    # 判断是否为 PointObject (多边形/样条)
    is_geometry = isinstance(obj, c4d.PointObject)

    # 决定是否包含半径 (即使用包围盒算法 vs Mp点算法)
    # 1. 底部对齐：必须包含半径才能找到底部
    # 2. 生成器对象 (非多边形，但有几何意义)：MagicCenter 倾向于使用包围盒中心
    # 3. 普通 Null 组：通常使用 Mp 平均 (保持 include_rad=False)
    # 但如何区分 "普通 Null" 和 "生成器"？
    # 在 C4D 中，生成器通常也是 BaseObject，CheckType 可以区分，但种类繁多。
    # 简单判定：如果对象不是 PointObject，我们假设它是生成器/组。

    # 混合策略：
    # - 底部对齐：强制 BBox
    # - 非底部对齐：
    #   - 多边形/样条：仅 Mp (include_rad=False)
    #   - 普通 Null (c4d.Onull): 仅 Mp (include_rad=False) -> 修复 Null_01 偏差
    #   - 生成器 (如细分/挤压): 强制 BBox (include_rad=True) -> 修复细分/挤压偏差

    if align_bottom:
        use_bbox = True
    else:
        # 如果是几何体或普通Null，用 Mp；否则（生成器），用 BBox
        if is_geometry or obj.CheckType(c4d.Onull):
            use_bbox = False
        else:
            use_bbox = True

    # 1. 收集自身 (如果是几何体)
    if is_geometry or obj.GetRad() != c4d.Vector(0):
        mg = obj.GetMg()
        mp = obj.GetMp()

        if use_bbox:
            rad = obj.GetRad()
            rx, ry, rz = rad.x, rad.y, rad.z
            mx, my, mz = mp.x, mp.y, mp.z
            points_to_calc.extend([
                mg * c4d.Vector(mx-rx, my-ry, mz-rz),
                mg * c4d.Vector(mx+rx, my-ry, mz-rz),
                mg * c4d.Vector(mx-rx, my+ry, mz-rz),
                mg * c4d.Vector(mx+rx, my+ry, mz-rz),
                mg * c4d.Vector(mx-rx, my-ry, mz+rz),
                mg * c4d.Vector(mx+rx, my-ry, mz+rz),
                mg * c4d.Vector(mx-rx, my+ry, mz+rz),
                mg * c4d.Vector(mx+rx, my+ry, mz+rz)
            ])
        else:
            points_to_calc.append(mg * mp)

    # 2. 递归收集子级
    # 策略：如果父级决定使用 BBox 模式，那么子级收集时也应该开启 include_rad=True，
    # 这样才能获得整个层级的精确包围盒中心。

    force_children = not is_geometry

    if include_children or force_children:
        CollectChildrenMps(obj, points_to_calc, include_rad=use_bbox)

    return CalculateCenter(points_to_calc, align_bottom=align_bottom)

def CollectAllChildren(obj, list_obj):
    """递归收集所有子对象"""
    for child in obj.GetChildren():
        list_obj.append(child)
        CollectAllChildren(child, list_obj)

def GetHierarchyDepth(obj):
    """获取对象的层级深度"""
    depth = 0
    curr = obj
    while curr.GetUp():
        depth += 1
        curr = curr.GetUp()
    return depth

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc: return

    # 使用 GETACTIVEOBJECTFLAGS_CHILDREN 标志以确保能获取到对象管理器中选中的所有对象
    # 即使是折叠的组内的对象
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN | c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if not selection:
        return

    qualifier = GetInputQualifiers()
    is_shift = (qualifier & c4d.QSHIFT) != 0
    is_ctrl = (qualifier & c4d.QCTRL) != 0
    is_alt = (qualifier & c4d.QALT) != 0

    # 新增组合键: Ctrl + Alt -> 对齐底部
    is_ctrl_alt = is_ctrl and is_alt

    mode = "HIERARCHY"
    if is_ctrl_alt:
        mode = "HIERARCHY_BOTTOM"
    elif is_alt:
        mode = "SELECTION"
    elif is_shift:
        mode = "OBJECT"
    elif is_ctrl:
        mode = "CHILDREN"

    # 性能优化: 暂停所有线程，防止视图频繁更新
    c4d.StopAllThreads()

    doc.StartUndo()

    try:
        for obj in selection:
            # 组件模式对齐 (Alt)
            # 如果是 Ctrl+Alt，则忽略组件模式，强制使用底部对齐逻辑
            has_component_selection = False
            if not is_ctrl_alt and isinstance(obj, c4d.PointObject):
                if obj.GetPointS().GetCount() > 0:
                    has_component_selection = True
                elif isinstance(obj, c4d.PolygonObject):
                    if obj.GetPolygonS().GetCount() > 0 or obj.GetEdgeS().GetCount() > 0:
                        has_component_selection = True

            if mode == "SELECTION":
                if has_component_selection:
                    points_to_calc = GetSelectionPointsGlobal(obj)
                    center = CalculateCenter(points_to_calc)
                    if center is not None:
                        SetAxisCenter(doc, obj, center)
                    continue

                # Alt 但无组件选择 -> 对齐父级
                parent = obj.GetUp()
                if parent:
                    child_mg = obj.GetMg()
                    target_pos = child_mg.off
                    SetAxisCenter(doc, parent, target_pos)
                continue

            # --- 对象模式对齐 ---

            if mode == "OBJECT":
                # Shift: 仅自身
                center = GetObjectCenter(obj, include_children=False)
                if center is not None:
                    SetAxisCenter(doc, obj, center)

            elif mode == "CHILDREN":
                # Ctrl: 仅子级 (移动父对象到子级中心)
                mp_points = []
                CollectChildrenMps(obj, mp_points, include_rad=False)
                center = CalculateCenter(mp_points)
                if center is not None:
                    SetAxisCenter(doc, obj, center)

            elif mode == "HIERARCHY_BOTTOM":
                # Ctrl + Alt: 底部对齐 (仅移动所选对象的轴心，基于自身及子级整体)
                # 逻辑：计算对象及其所有子级的整体包围盒底部，仅将当前对象的轴心移动到该位置
                # 即使同时选择了父级和子级，也分别处理各自的"整体"

                center = GetObjectCenter(obj, include_children=True, align_bottom=True)
                if center is not None:
                    SetAxisCenter(doc, obj, center)

            else: # mode == "HIERARCHY" (Default)
                # 默认模式：递归处理所有子级轴心，最后处理父级

                # 1. 收集所有涉及的对象
                hierarchy_list = [obj]
                CollectAllChildren(obj, hierarchy_list)

                # 2. 按深度排序（倒序：深层 -> 浅层）
                hierarchy_list.sort(key=GetHierarchyDepth, reverse=True)

                # 3. 逐个处理
                for target_obj in hierarchy_list:
                    # 策略：
                    # - 如果是 PointObject (多边形/样条)，将其轴心重置到自身几何中心
                    # - 如果是 Generator/Null (组)，将其轴心重置到子级中心

                    if isinstance(target_obj, c4d.PointObject):
                         center = GetObjectCenter(target_obj, include_children=False)
                    else:
                         center = GetObjectCenter(target_obj, include_children=True)

                    if center is not None:
                        SetAxisCenter(doc, target_obj, center)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        doc.EndUndo()
        c4d.EventAdd()

if __name__ == '__main__':
    main()
