# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Mute Layer
Name-ZH:静音层
Description-US:CLOSE View\Render\Manager\Locked\Animation\Generators\Deformers\Expressions\Xref
Description-ZH:关闭 View\Render\Manager\Locked\Animation\Generators\Deformers\Expressions\Xref
"""

import c4d

# Functions
def GetNextItem(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectLayers():
    def IterateLayers(op):
        layerList = [] # Initialize an array for collecting layers
        if op is None: # If there is no layer
            return # This is over
        while op: # While there is an item
            layerList.append(op) # Add layer to layer list
            op = GetNextItem(op) # Get next layer
        return layerList # Return layers

    doc = c4d.documents.GetActiveDocument() # Get active document
    layerRoot = doc.GetLayerObjectRoot() # Get layer object root
    layers = layerRoot.GetChildren() # Get layers
    if layers == []: # Check if there is no any layer
        return None # Return none
    else: # If there is any layer
        startLayer = layers[0] # Get start layer for iterating through all layers
        return IterateLayers(startLayer) # Return collection of all layers

def DisableLayerVisibility():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    layers = CollectLayers()
    selectedLayers = []
    for l in layers:
        if l.GetBit(c4d.BIT_ACTIVE):
            selectedLayers.append(l)

    for s in selectedLayers:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo command for changing something
        if s[c4d.ID_LAYER_VIEW] == 0 and s[c4d.ID_LAYER_RENDER] == 0 and s[c4d.ID_LAYER_MANAGER] == 0 and s[c4d.ID_LAYER_LOCKED] == 1 and s[c4d.ID_LAYER_ANIMATION] == 0 and s[c4d.ID_LAYER_GENERATORS] == 0 and s[c4d.ID_LAYER_DEFORMERS] == 0 and s[c4d.ID_LAYER_EXPRESSIONS] == 0 and s[c4d.ID_LAYER_XREF] == 0:
            s[c4d.ID_LAYER_VIEW] = 1
            s[c4d.ID_LAYER_RENDER] = 1
            s[c4d.ID_LAYER_MANAGER] = 1
            s[c4d.ID_LAYER_LOCKED] = 0
            s[c4d.ID_LAYER_ANIMATION] = 1
            s[c4d.ID_LAYER_GENERATORS] = 1
            s[c4d.ID_LAYER_DEFORMERS] = 1
            s[c4d.ID_LAYER_EXPRESSIONS] = 1
            s[c4d.ID_LAYER_XREF] = 1
        else:
            s[c4d.ID_LAYER_VIEW] = 0
            s[c4d.ID_LAYER_RENDER] = 0
            s[c4d.ID_LAYER_MANAGER] = 0
            s[c4d.ID_LAYER_LOCKED] = 1
            s[c4d.ID_LAYER_ANIMATION] = 0
            s[c4d.ID_LAYER_GENERATORS] = 0
            s[c4d.ID_LAYER_DEFORMERS] = 0
            s[c4d.ID_LAYER_EXPRESSIONS] = 0
            s[c4d.ID_LAYER_XREF] = 0
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

def main():
    DisableLayerVisibility()

# Execute the main function
if __name__ == '__main__':
    main()