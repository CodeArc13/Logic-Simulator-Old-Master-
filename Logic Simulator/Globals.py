import pygame
from Consts import WINDOWWIDTH, WINDOWHEIGHT, TOPBAR

class SelectedBlockType(object):
    type = 1 #default is wire blocks
    def set(type):
        SelectedBlockType.type = type
    def get():
        return SelectedBlockType.type

class EditCounter(object):
    editCount = 0 #number of edits so far, in entire program session
    def inc():
        EditCounter.editCount += 1
    def get():
        return EditCounter.editCount

class CameraBlocksX(object): #top left corner of screen
    x = 0 #left of current draw area, other end is boardWidth + CameraBlocksX, IN Blocks
    pixX = 0
    def inc():
        CameraBlocksX.x += 1
    def dec():
        CameraBlocksX.x -= 1
    def set(x):
        CameraBlocksX.x = x
    def get():
        return CameraBlocksX.x
    def setPix(x):
        CameraBlocksX.pixX = x
    def getPix():
        return CameraBlocksX.pixX

class CameraBlocksY(object): #top left corner of screen
    y = 0 #top of current draw area, other end is boardHeight + CameraBlocksY, IN Blocks
    pixY = 0
    def inc():
        CameraBlocksY.y += 1
    def dec():
        CameraBlocksY.y -= 1
    def set(y):
        CameraBlocksY.y = y
    def get():
        return CameraBlocksY.y
    def setPix(y):
        CameraBlocksY.pixY = y
    def getPix():
        return CameraBlocksY.pixY
    #def convert():

class BoxSize(object): 
    boxSize = 10 #pixels
    def inc():
        BoxSize.boxSize += 5
    def dec():
        BoxSize.boxSize -= 5
    def set(sz):
        BoxSize.boxSize = sz
    def get():
        return BoxSize.boxSize

class BoardHeight(object):
    lastBoardHeight = 0
    boardHeight = int(WINDOWHEIGHT / BoxSize.get()) + 1 #blocks
    def set(height):
        BoardHeight.lastBoardHeight = BoardHeight.boardHeight
        BoardHeight.boardHeight = height
    def get():
        return BoardHeight.boardHeight
    def last():
        return BoardHeight.boardHeight

class BoardWidth(object):
    lastBoardWidth = 0
    boardWidth = int(WINDOWWIDTH / BoxSize.get()) + 1
    def set(width):
        BoardWidth.lastBoardWidth = BoardWidth.boardWidth
        BoardWidth.boardWidth = width
    def get():
        return BoardWidth.boardWidth
    def last():
        return BoardWidth.lastBoardWidth

class Xmargin(object):
    xMargin = 0#int((WINDOWWIDTH - (BoardWidth.get() * BoxSize.get())) / 2)
    def get():
        return Xmargin.xMargin

class Ymargin(object):
    yMargin = TOPBAR#int((WINDOWHEIGHT - (BoardHeight.get() * BoxSize.get())))# / 2)
    def get():
        return Ymargin.yMargin

class Border(object):
    #border = (Xmargin.get() - 2, Ymargin.get() - 2, (BoardWidth.get() * BoxSize.get()) + 3, (BoardHeight.get() * BoxSize.get()) + 3)
    border = (0, Ymargin.get() - 2, WINDOWWIDTH, 1)
    def get():
        return Border.border

def leftTopCoordsOfBox(boxx, boxy):  #screen coords
    #Convert block coordinates to pixel coordinates
    left = boxx * BoxSize.get() + Xmargin.get()  #screen coords
    top = boxy * BoxSize.get() + Ymargin.get()  #screen coords
    return (left, top)  #screen coords 

#Linear search
#def getBoxAtPixel(x, y): #screen coords
#    #print 'in get box'
#    for boxx in range(BoardWidth.get()):
#        for boxy in range(BoardHeight.get()):
#            left, top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
#            boxRect = pygame.Rect(left, top, BoxSize.get(), BoxSize.get()) #screen coords
#            if boxRect.collidepoint(x, y):  #screen coords
#                return (boxx, boxy) #screen coords
#    return (None, None)

#Binary search #using lines
def getBoxAtPixel(x, y): #mouse coords in pixels

    rowS = 0                    #Row start
    rowE = BoardHeight.get()    #Row end

    while rowS <= rowE:

        rowMid = int(rowS + (rowE - rowS) / 2)
        left, top = leftTopCoordsOfBox(0, rowMid)
        boxRect = pygame.Rect(left, top, BoxSize.get() * BoardWidth.get(), BoxSize.get()) #screen coords
        if boxRect.collidepoint(x, y):  #screen coords

            colS = 0                    #Col start
            colE = BoardWidth.get()     #Col end

            while colS <= colE:
            #if mouse is somewhere in this row bin search it
                
                colMid = int(colS + (colE - colS) / 2)
                left, top = leftTopCoordsOfBox(colMid, rowMid)
                boxRect = pygame.Rect(left, top, BoxSize.get(), BoxSize.get()) #screen coords
                if boxRect.collidepoint(x, y):  #screen coords
                    return colMid, rowMid

                elif left < x:
                    colS = colMid + 1
                else:
                    colE = colMid - 1


        elif top < y:
            rowS = rowMid + 1
        else:
            rowE = rowMid - 1

    return (None, None)


#XMARGIN = int((WINDOWWIDTH - (BoardWidth.get() * BoxSize.get())) / 2)
#YMARGIN = int((WINDOWHEIGHT - (BoardHeight.get() * BoxSize.get())) / 2)
#GRIDBACKGROUND = (XMARGIN - GAPSIZE, YMARGIN - GAPSIZE, (BoardWidth.get() * (BoxSize.get() + GAPSIZE)) + GAPSIZE, (BoardHeight.get() * (BoxSize.get() + GAPSIZE)) + GAPSIZE)
#BORDER = (XMARGIN - 2, YMARGIN - 2, (BoardWidth.get() * BoxSize.get()) + 3, (BoardHeight.get() * BoxSize.get()) + 3)

#possible use for moveing camera by pixels instead of blocks
    #cameraPixX = 0 #top left of current draw area, other end is board width, IN pixels
    #cameraPixY = 0 #top left of current draw area, other end is board height

