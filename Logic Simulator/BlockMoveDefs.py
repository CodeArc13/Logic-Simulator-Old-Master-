from Sto import mainDict, WSet, TSet
from Display import drawRect
from Globals import CameraBlocksX, CameraBlocksY, leftTopCoordsOfBox
from Const import EMPTYBLOCKBORDER, EMPTYBLOCK, BOXSIZE, BOARDWIDTH, BOARDHEIGHT


def clearDrawArea(): #only clear filled blocks not empty blocks, should be quicker than redrawing entire screen for every move
    for wire in WSet: #world coords
        if (wire[0] >= CameraBlocksX.getX() and wire[0] <= CameraBlocksX.getX() + BOARDWIDTH - 1) and \
            (wire[1] >= CameraBlocksY.getY() and wire[1] <= CameraBlocksY.getY() + BOARDHEIGHT - 1): #checks if block is on screen
            location = mainDict[wire].blockLocSize #screen coords
            clearBlock(location)
            mainDict[wire].onScreen = True
        else: #if block off screen
            location = mainDict[wire].blockLocSize #screen coords
            clearBlock(location)
            mainDict[wire].onScreen = False        
    for transistor in TSet: #world coords
        if (transistor[0] >= CameraBlocksX.getX() and transistor[0] <= CameraBlocksX.getX() + BOARDWIDTH - 1) and \
            (transistor[1] >= CameraBlocksY.getY() and transistor[1] <= CameraBlocksY.getY() + BOARDHEIGHT - 1):
            location = mainDict[transistor].blockLocSize #screen coords
            clearBlock(location)
            mainDict[transistor].onScreen = True    
        else: #if block off screen
            location = mainDict[transistor].blockLocSize #screen coords
            clearBlock(location)
            mainDict[transistor].onScreen = False  
            

def clearBlock(loc): #helper def for clearDrawArea to compact repeating code
    #drawRect(EMPTYBLOCKBORDER, loc) #clears yellow edge left from transistor, prevents haveing to redraw background
    drawRect(EMPTYBLOCK, (loc[0], loc[1], BOXSIZE, BOXSIZE)) #screen coords


def moveBlocks():
    for block in mainDict:
        mainDict[block].repositionOnScreen()