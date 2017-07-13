from Const import BOXSIZE, GAPSIZE, XMARGIN, YMARGIN


class SelectedBlockType(object):
    type = 1 #default is wire blocks
    def setType(type):
        SelectedBlockType.type = type
    def getType():
        return SelectedBlockType.type

class EditCounter():
    editCount = 0 #number of edits so far, in entire program session
    def incEditCount():
        EditCounter.editCount += 1
    def getEditCount():
        return EditCounter.editCount

class CameraBlocksX():
    x = 0 #left of current draw area, other end is boardWidth + CameraBlocksX, IN Blocks
    def incX():
        CameraBlocksX.x += 1
    def decX():
        CameraBlocksX.x -= 1
    def getX():
        return CameraBlocksX.x

class CameraBlocksY():
    y = 0 #top of current draw area, other end is boardHeight + CameraBlocksY, IN Blocks
    def incY():
        CameraBlocksY.y += 1
    def decY():
        CameraBlocksY.y -= 1
    def getY():
        return CameraBlocksY.y

def leftTopCoordsOfBox(boxx, boxy):  #screen coords
    #Convert block coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN  #screen coords
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN  #screen coords
    return (left, top)  #screen coords

#possible use for moveing camera by pixels instead of blocks
    #cameraPixX = 0 #top left of current draw area, other end is board width, IN pixels
    #cameraPixY = 0 #top left of current draw area, other end is board height

