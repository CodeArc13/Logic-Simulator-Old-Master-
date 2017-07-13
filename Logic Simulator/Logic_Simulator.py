import pygame, sys
from pygame.locals import *
from Const import *
from Sto import *
from Globals import *
from Display import *
from WirePath import WirePath
from WireBlock import WireBlock
from TransistorBlock import TransistorBlock

         
def main():
    PROCESSRATE = 100 #process cycles at a set rate in milliseconds
    elapsedTime = 0 #ammount of time in milliseconds since late procress cycle

    leftMouseDown = False
    middleMouse = False
    rightMouseDown = False

    firstMoveMiddle = True #set false after inital move with middle mouse down

    movementTotalX = 0
    movementTotalY = 0
    totalLeft = 0
    totalRight = 0
    totalUp = 0
    totalDown = 0

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
     
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render('FPS', True, YELLOW)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (33, 25)
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    boxx, boxy = None, None
  
    pygame.display.set_caption('Logic Simulator')

    drawRect(BGCOLOR, GRIDBACKGROUND)
    
    drawEmptyBoard()

    while True: # main game loop    
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_1:
                    SelectedBlockType.setType(1)
                    print ('selected wire blocks')
                elif event.key == K_2:
                    SelectedBlockType.setType(2)
                    print ('selected left transistor blocks')
                elif event.key == K_3:
                    SelectedBlockType.setType(3)
                    print ('selected right transistor blocks')
                elif event.key == K_4:
                    SelectedBlockType.setType(4)
                    print ('selected up transistor blocks')
                elif event.key == K_5:
                    SelectedBlockType.setType(5)
                    print ('selected down transistor blocks')
            elif event.type == MOUSEMOTION:
                if leftMouseDown ^ rightMouseDown: #(Xor)prevents motion with none or both buttons pressed from triggering events
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                if middleMouse:
                    if firstMoveMiddle is False:
                        relativePosition = pygame.mouse.get_rel()
                        movementTotalX += relativePosition[0]
                        movementTotalY += relativePosition[1]
                    if relativePosition[0] < 0:
                        totalLeft += abs(relativePosition[0])
                        totalRight = 0
                    if relativePosition[0] > 0:
                        totalRight += abs(relativePosition[0])
                        totalLeft = 0
                    if relativePosition[1] < 0:
                        totalUp += abs(relativePosition[1])
                        totalDown = 0
                    if relativePosition[1] > 0:
                        totalDown += abs(relativePosition[1])
                        totalUp = 0
                    if totalLeft >= TOTALBOXSIZE:
                        #cameraPixX += TOTALBOXSIZE
                        CameraBlocksX.incX()
                        totalLeft = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalRight >= TOTALBOXSIZE:
                        #cameraPixX -= TOTALBOXSIZE
                        CameraBlocksX.decX()
                        totalRight = 0
                        clearDrawArea()
                        moveBlocks()
                    if totalUp >= TOTALBOXSIZE:
                        #cameraPixY += TOTALBOXSIZE
                        CameraBlocksY.incY()
                        totalUp = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalDown >= TOTALBOXSIZE:
                        #cameraPixY -= TOTALBOXSIZE
                        CameraBlocksY.decY()
                        totalDown = 0
                        clearDrawArea()
                        moveBlocks()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    leftMouseDown = True
                elif event.button == 2:
                    middleMouse = True
                    firstMoveMiddle = False
                    relativePosition = pygame.mouse.get_rel()
                    relativePosition = (0, 0)
                    movementTotalX = 0
                    movementTotalY = 0
                    totalLeft = 0
                    totalRight = 0
                    totalUp = 0
                    totalDown = 0
                elif event.button == 3:
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    rightMouseDown = True
                elif event.button == 4:
                    print('mouse wheel up')
                elif event.button == 5:
                    print('mouse wheel down')
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1: #add block
                    leftMouseDown = False
                elif event.button == 2: #move camera
                    middleMouse = False
                    firstMoveMiddle = True
                elif event.button == 3: #delete block
                    rightMouseDown = False

        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if leftMouseDown and rightMouseDown == False: #prevents event if both buttons pressed
                setBlock(boxx, boxy)
            elif rightMouseDown and leftMouseDown == False:
                deleteBlock(boxx, boxy)               

        #TRANSISTOR AND WIRE LOGIC PROCESSING HERE
        elapsedTime += FPSCLOCK.get_time()
        if elapsedTime >= PROCESSRATE:
            elapsedTime = 0
            
            if WireBlock.getWireBlockDeleted() == False:#if wireBlockDeleted is true then do not process transistors this tick
                for operateTransistorKey in TSet:
                    mainDict[operateTransistorKey].Operation()
            else: #if True
                WireBlock.setWireBlockDeleted(False)

            for processWirePathsKey in wirePathDict:
                wirePathDict[processWirePathsKey].processWirePath()                   
            #turn off every wire, then turn on only the wires that are comming on or staying on in this cycle that way we wont need to specifically turn off wires
            #for turnOffWiresKey in WSet:
            #    mainDict[turnOffWiresKey].turnOff()       
        
            #process wires here instead of in transistor objects
            #for processWiresKey in TSet: #loop through all transistors
            #    if mainDict[processWiresKey].getState(): #check if current transistor is switched ON, if OFF skip
                
            #        #ask current transistor to return list of connected wires that have not been processed this tick (add def to transistor and wire classes that filters these wires)
            #        #add returned list to set/queue
            #        for transistorWire in mainDict[processWiresKey].returnConnectedUnprocessedWires():
            #            unprocessedWires.add(transistorWire)                 
            #        #loop through each wire in set
            #        while unprocessedWires: #while set/queue is not empty:
            #            currentWire = unprocessedWires.pop()
            #            mainDict[currentWire].turnOn() #turn on current wire setTick/processed-boolean
            #            for wire in mainDict[currentWire].returnConnectedUnprocessedWires(): #ask current wire to return list of surrounding unprocessed wires and add to set
            #                unprocessedWires.add(wire)
            #doDraws = True
        
        #draw only the blocks in the current draw area here
        #if doDraws == True:
        #    for drawWire in WSet:
        #        draw = mainDict[drawWire].getDrawTuple()
        #        pygame.draw.rect(DISPLAYSURF, draw[0], draw[1])
        #    for drawTransistor in TSet:
        #        draw = mainDict[drawTransistor].getDrawTuple()
        #        pygame.draw.rect(DISPLAYSURF, draw[0], draw[1])
        #    doDraws = False
        #Redraw the screen and wait a clock tick.

        if WireBlock.getWireBlockDeleted() == False:#if wireBlockdeleted is true do not increment tick this tick or update display           
            pygame.display.update()
        
        FPSCLOCK.tick(FPS)
        drawRect(BLACK, (0, 0, 78, 36)) #remove last blitted FPS
        textSurfaceObj = fontObj.render('%.2f' % FPSCLOCK.get_fps(), True, YELLOW)
        blitToSurf(textSurfaceObj, textRectObj)


def getBoxAtPixel(x, y): #screen coords
    #print 'in get box'
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)  #screen coords
            if boxRect.collidepoint(x, y):  #screen coords
                return (boxx, boxy) #screen coords
    return (None, None)


def drawEmptyBoard():
    for boxx in range(BOARDWIDTH): #screen coords
        for boxy in range(BOARDHEIGHT): #screen coords
            left, top = leftTopCoordsOfBox(boxx, boxy) #screen coords
            #WSet.add((boxx, boxy))
            #mainDict[boxx, boxy] = WireBlock(boxx, boxy)
            drawRect(EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE)) #screen coords


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
    drawRect(EMPTYBLOCKBORDER, loc) #clears yellow edge left from transistor, prevents haveing to redraw background
    drawRect(EMPTYBLOCK, (loc[0] + 1, loc[1] + 1, BOXSIZE, BOXSIZE)) #screen coords


def moveBlocks():
    for block in mainDict:
        mainDict[block].repositionOnScreen()


def deleteBlock(boxx, boxy): #screen coords
    worldX, worldY = boxx + CameraBlocksX.getX(), boxy + CameraBlocksY.getY()
    if (worldX, worldY) in mainDict:
        if (worldX, worldY) in TSet:
            transistorsPaths = mainDict[worldX, worldY].getWirePaths()
            for path in transistorsPaths:
                wirePathDict[path].remTrans((worldX, worldY))
                if wirePathDict[path].getTransTotal() == 0:
                    wirePathDict[path].turnOff()
            TSet.remove((worldX, worldY))
        else:
            try: #if no key don't worry, this is for orphaned wirepaths (wirepaths with no transistor outputs attached)
                wirePathDict[mainDict[worldX, worldY].getWirePathID()].turnOff()
                WireBlock.setWireBlockDeleted(True)                    
            except KeyError:
                pass
            WSet.remove((worldX, worldY))  
        del mainDict[worldX, worldY]
        left, top = leftTopCoordsOfBox(boxx, boxy) #screen coords
        drawRect(EMPTYBLOCKBORDER, (left - 1, top - 1, TOTALBOXSIZE, TOTALBOXSIZE)) #clears yellow edge left from transistor, prevents haveing to redraw background
        drawRect(EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE))
        mapWirePaths() #wirePathMapping def here
            

def setBlock(boxx, boxy): #screen coords
    worldX, worldY = boxx + CameraBlocksX.getX(), boxy + CameraBlocksY.getY()
    blockType = SelectedBlockType.getType()
    if blockType == 1:
        if (worldX, worldY) not in mainDict:
            WSet.add((worldX, worldY))
            mainDict[worldX, worldY] = WireBlock(boxx, boxy) #send in screen coords to block object constructors
            mapWirePaths() #wirePathMapping def here
    elif blockType == 2: #left input transistor
        if (worldX, worldY) not in mainDict:
            TSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(LEFT, boxx, boxy, \
                LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY)
            mapWirePaths() #wirePathMapping def here
    elif blockType == 3: #right input transistor
        if (worldX, worldY) not in mainDict: 
            TSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(RIGHT, boxx, boxy, \
                RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY)
            mapWirePaths() #wirePathMapping def here
    elif blockType == 4: #up input transistor
        if (worldX, worldY) not in mainDict: 
            TSet.add((worldX, worldY)) 
            mainDict[worldX, worldY] = TransistorBlock(UP, boxx, boxy, \
                UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY)
            mapWirePaths() #wirePathMapping def here
    elif blockType == 5: #down input transistor
        if (worldX, worldY) not in mainDict:
            TSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(DOWN, boxx, boxy, \
                DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY)
            mapWirePaths() #wirePathMapping def here


def mapWirePaths():
    WirePath.resetWirePathID()
    transistorSearchSet = set()
    wireSearchSet = set()
    wirePathDict.clear() #clear dictionary ready for new edit mapping
    for transistor in TSet:
        mainDict[transistor].clearWirePathIDs() #clear pathIDs 
        transistorOutputList = mainDict[transistor].returnConnectedWires()
        for outputWire in transistorOutputList:
            if mainDict[outputWire].getEditCount() < EditCounter.getEditCount():
                transistorSearchSet.add(outputWire) #add to search set if not edited this edit
            else:
                mainDict[transistor].addWirePathID(mainDict[outputWire].getWirePathID()) #add wire's pathID to current transistor if edited this edit#
                wirePathDict[mainDict[outputWire].getWirePathID()].addTrans(transistor) #add transistor to wirepath that output wire belongs too
            while transistorSearchSet: #not empty
                currentTransistorOutputWire = transistorSearchSet.pop()
                if mainDict[currentTransistorOutputWire].getEditCount() < EditCounter.getEditCount(): #search wirepath else go to next output wire/transistor
                    wireSearchSet.add(currentTransistorOutputWire)
                    wirePathDict[WirePath.currentWirePathID] = WirePath(WirePath.currentWirePathID) #add a new wirepath set with key of current ID
                    while wireSearchSet: #not empty
                        currentWire = wireSearchSet.pop()
                        for wire in mainDict[currentWire].returnConnectedUneditedWires():
                            wireSearchSet.add(wire)
                        mainDict[currentWire].setEditCount(EditCounter.getEditCount())
                        mainDict[currentWire].setWirePathID(WirePath.currentWirePathID)                        
                        wirePathDict[WirePath.currentWirePathID].addToPath(currentWire)#assign Current wire location to wirepath dictionary for current setValue of wirepathID
                    mainDict[transistor].addWirePathID(WirePath.currentWirePathID)
                    wirePathDict[WirePath.currentWirePathID].addTrans(transistor)
                    WirePath.incrementCurrentWirePathID()                   
    EditCounter.incEditCount()
        

#def drawBoard(dict):
#    for boxx in xrange(BOARDWIDTH):
#        for boxy in xrange(BOARDHEIGHT):
#            left, top = leftTopCoordsOfBox(boxx, boxy)
#            if type(board[boxx + 1, boxy + 1]) is EmptyBlock:
#                pygame.draw.rect(DISPLAYSURF, RED, (left - 1, top - 1, BOXSIZE + 2, BOXSIZE + 2), 1) #clears yellow edge left from transistor, prevents haveing to redraw background
#                pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE))
#            elif type(board[boxx + 1, boxy + 1]) is WireBlock:
#                pygame.draw.rect(DISPLAYSURF, WIREBLOCK, (left - 1, top - 1, BOXSIZE + 2, BOXSIZE + 2))
#            elif type(board[boxx + 1, boxy + 1]) is TransistorBlock:
#                pygame.draw.rect(DISPLAYSURF, TRANSISTORBLOCK, (left - 1, top - 1, BOXSIZE + 2, BOXSIZE + 2))

#def drawIcon(shape, color, boxx, boxy):
#    quarter = int(BOXSIZE * 0.25) # syntactic sugar
#    half =    int(BOXSIZE * 0.5)  # syntactic sugar

#    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
#    # Draw the shapes
#    if shape == SQUARE:
#        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half)) ##use for drawing wires and transistors

if __name__ == '__main__':
    main()



