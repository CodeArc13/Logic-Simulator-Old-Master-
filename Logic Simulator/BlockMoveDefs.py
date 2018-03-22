from Sto import mainDict, WSet, TSet
from Display import drawRect
from Globals import CameraBlocksX, CameraBlocksY, BoxSize, BoardHeight, BoardWidth, leftTopCoordsOfBox
from Consts import WINDOWWIDTH, WINDOWHEIGHT, EMPTYBLOCKBORDER, EMPTYBLOCK, TOPBAR


def clearDrawArea(): #only clear filled blocks not empty blocks, should be quicker than redrawing entire screen for every move
    for block in mainDict: #world coords
        if checkOnScreen(mainDict[block].getLocation()): #checks if block is on screen
            clearBlock(mainDict[block].blockLocSize)
            mainDict[block].onScreen = True
        else: #if block off screen
            clearBlock(mainDict[block].blockLocSize)
            mainDict[block].onScreen = False      
    #for transistor in TSet: #world coords
    #    if checkOnScreen(transistor):
    #        location = mainDict[transistor].blockLocSize #screen coords
    #        clearBlock(location)
    #        mainDict[transistor].onScreen = True    
    #    else: #if block off screen
    #        location = mainDict[transistor].blockLocSize #screen coords
    #        clearBlock(location)
    #        mainDict[transistor].onScreen = False  
            
def clearBlock(loc): #helper def for clearDrawArea to compact repeating code
    drawRect(EMPTYBLOCK, (loc[0], loc[1], BoxSize.get(), BoxSize.get())) #screen coords

def moveBlocks():
    for block in mainDict:
        mainDict[block].repositionOnScreen()

def zoomIn():
    if BoxSize.get() < 60: #prevent BoxSize.get() from being larger than 60px
        BoxSize.inc()
        BoardHeight.set(int(WINDOWHEIGHT / BoxSize.get()) + 1) #fills screen
        BoardWidth.set(int(WINDOWWIDTH / BoxSize.get()) + 1)
        #if BoxSize.get() == 60:
        #    CameraBlocksX.set(CameraBlocksX.get() + 1)
        #    CameraBlocksY.set(CameraBlocksY.get() + 1)
         
def zoomOut():
    if BoxSize.get() > 5: #prevent BoxSize.get() going into negative pixel size
        BoxSize.dec()         
        BoardHeight.set(int(WINDOWHEIGHT / BoxSize.get()) + 1)
        BoardWidth.set(int(WINDOWWIDTH / BoxSize.get()) + 1)
        #if BoxSize.get() == 55:
        #    CameraBlocksX.set(CameraBlocksX.get() - 1)
        #    CameraBlocksY.set(CameraBlocksY.get() - 1)

def zoomBlocks():
    for block in mainDict:
        if checkOnScreen(mainDict[block].getLocation()):
            mainDict[block].onScreen = True
            mainDict[block].repositionOnScreen()
        else:
            mainDict[block].onScreen = False
        
def checkOnScreen(loc):  #checks if block is on screen
    return (loc[0] >= CameraBlocksX.get() and loc[0] <= CameraBlocksX.get() + BoardWidth.get() - 1) and \
            (loc[1] >= CameraBlocksY.get() and loc[1] <= CameraBlocksY.get() + BoardHeight.get() - 1 - (TOPBAR / BoxSize.get()))