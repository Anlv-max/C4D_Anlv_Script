# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Clean Curve
Name-ZH:清洁动画曲线
Description-US:[Default] Clean selected curves [SHIFT+Click] Clean the entire scene [CTRL+Click] Clean the entire scene, excluding selected objects.
Description-ZH:[默认] 清洁选中对象的无效曲线 [SHIFT+单击] 清洁整个场景 [CTRL-单击] 清洁整个场景，但排除选中对象
"""

import c4d
from c4d import gui

def remove_unused_frames(obj):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    for track in obj.GetCTracks():
        curve = track.GetCurve()
        if curve is not None and curve.GetKeyCount() > 1:
            first_keyframe = curve.GetKey(0)
            last_keyframe = curve.GetKey(curve.GetKeyCount() - 1)
            if first_keyframe.GetValue() == last_keyframe.GetValue():
                track.Remove()

def script1():
    doc.StartUndo()
    sel = doc.GetSelection()
    for obj in sel:
        remove_unused_frames(obj)
    doc.EndUndo()
    c4d.EventAdd()

def script2():
    c4d.CallCommand(100004794) # Invert Selection
    doc.StartUndo()
    sel = doc.GetSelection()
    for obj in sel:
        remove_unused_frames(obj)
    doc.EndUndo()
    c4d.EventAdd()

def script3():
    c4d.CallCommand(100004766) # Select All
    doc.StartUndo()
    sel = doc.GetSelection()
    for obj in sel:
        remove_unused_frames(obj)
    doc.EndUndo()
    c4d.CallCommand(100004767) # Deselect All
    c4d.EventAdd()

def script4():
    return "Alt"

def main():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            result = script3()
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            result = script2()
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            result = script4()
        else:
            result = None
            script1()
        print(result)

if __name__=='__main__':
    main()