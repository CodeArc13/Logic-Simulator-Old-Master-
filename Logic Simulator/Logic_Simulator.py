import pygame, sys
from pygame.locals import *


FPS = 60 # frames per second, the general speed of the program
WINDOWWIDTH = 1000 # size of window's width in pixels
WINDOWHEIGHT = 1000 # size of windows' height in pixels
BOXSIZE = 15 # size of box height & width in pixels
GAPSIZE = 2 # size of gap between boxes in pixels
TOTALBOXSIZE = BOXSIZE + GAPSIZE
BOARDWIDTH = 50 # number of columns of blocks
BOARDHEIGHT = 50 # number of rows of blocks
BOARDHEIGHTPIX = BOARDHEIGHT * TOTALBOXSIZE
BOARDWIDTHPIX = BOARDWIDTH * TOTALBOXSIZE 
#assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

GRIDBACKGROUND = (XMARGIN - GAPSIZE, YMARGIN - GAPSIZE, (BOARDWIDTH * (BOXSIZE + GAPSIZE)) + GAPSIZE, (BOARDHEIGHT * (BOXSIZE + GAPSIZE)) + GAPSIZE)




#            R    G    B
BLACK    = (  0,   0,   0)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
DARKRED  = (55,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = RED
EMPTYBLOCK = BLACK
EMPTYBLOCKBORDER = RED
WIREBLOCKON = RED
WIREBLOCKOFF = DARKRED
TRANSISTORBLOCKON = YELLOW
TRANSISTORBLOCKOFF = ORANGE

LEFTSIDEX = -1 #left
LEFTSIDEY = 0
RIGHTSIDEX = 1 #right
RIGHTSIDEY = 0
UPSIDEX = 0 #up
UPSIDEY = -1
DOWNSIDEX = 0 #down
DOWNSIDEY = 1

#Transistor types
LEFT = 2
RIGHT = 3
UP = 4
DOWN = 5

ON = True #for operation of blocks
OFF = False

#dictionary of filled blocks (non-empty blocks)
mainDict = {}
#sets of filled blocks
transistorSet = set()
wireSet = set()


class Block: #base class of all block objects
    def __init__(self, boxx, boxy):
        pass
    def Operation(self): #takes the inputs from surrounding blocks
        pass
    def returnConnectedUnprocessedWires(self):
        pass
    def Output(self, queryingBlockX, queryingBlockY): #gives querying block the current state
        pass


class WireBlock(Block):
    def __init__(self, boxx, boxy): #screen coords
        self.boxx, self.boxy = (boxx + cameraBlocksX, boxy + cameraBlocksY) #world coords, screen coords. screen converted to world
        self.left, self.top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
        self.inputBlockL = (LEFTSIDEX + self.boxx, self.boxy) #world coords
        self.inputBlockR = (RIGHTSIDEX + self.boxx, self.boxy) #world coords
        self.inputBlockU = (self.boxx, UPSIDEY + self.boxy) #world coords
        self.inputBlockD = (self.boxx, DOWNSIDEY + self.boxy) #world coords
        self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
        self.onScreen = True
        self.processedThisTick = False
        self.state = OFF
        #print('world coordinates ' + str(self.boxx) + ', ' + str(self.boxy))

    #def initialSetup(self):
    #    if self.checkAroundWire():
    #        self.state = ON
    #        pygame.draw.rect(DISPLAYSURF, WIREBLOCKON, self.blockLocSize)
    #    else:
    #        self.state = OFF 
    #        pygame.draw.rect(DISPLAYSURF, WIREBLOCKOFF, self.blockLocSize)
    #def Operation(self): #takes the inputs from surrounding blocks
    #    if self.checkAroundWire():
    #        self.state = ON
    #        pygame.draw.rect(DISPLAYSURF, WIREBLOCKON, self.blockLocSize)
    #    else:
    #        self.state = OFF 
    #        pygame.draw.rect(DISPLAYSURF, WIREBLOCKOFF, self.blockLocSize)
    #def checkAroundWire(self): #checks if any blocks around wire are on
    #    if (self.inputBlockL in mainDict and mainDict[self.inputBlockL].Output(self.boxx, self.boxy)) or \
    #       (self.inputBlockR in mainDict and mainDict[self.inputBlockR].Output(self.boxx, self.boxy)) or \
    #       (self.inputBlockU in mainDict and mainDict[self.inputBlockU].Output(self.boxx, self.boxy)) or \
    #       (self.inputBlockD in mainDict and mainDict[self.inputBlockD].Output(self.boxx, self.boxy)): # == True): ^^^
    #        return ON
    #    else: #all blocks are off or empty
    #        return OFF
    def returnConnectedUnprocessedWires(self):
        self.unprocessedWireList = []
        if self.inputBlockL in wireSet: #check if block is a wire
            if not mainDict[self.inputBlockL].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.inputBlockL) #add wire to return list
        if self.inputBlockR in wireSet: #check if block is a wire
            if not mainDict[self.inputBlockR].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.inputBlockR) #add wire to return list
        if self.inputBlockU in wireSet: #check if block is a wire
            if not mainDict[self.inputBlockU].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.inputBlockU) #add wire to return list
        if self.inputBlockD in wireSet: #check if block is a wire
            if not mainDict[self.inputBlockD].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.inputBlockD) #add wire to return list
        return self.unprocessedWireList
    
    def getProcessedThisTick(self):
        return self.processedThisTick
    def turnOn(self):
        self.processedThisTick = True
        self.state = ON
        if self.onScreen:
            self.drawBlock(WIREBLOCKON)
    def turnOff(self):
        self.processedThisTick = False
        self.state = OFF
        if self.onScreen:
            self.drawBlock(WIREBLOCKOFF)

    def repositionOnScreen(self): #screen coords
        if self.onScreen:
            self.left, self.top = leftTopCoordsOfBox(self.boxx - cameraBlocksX, self.boxy - cameraBlocksY)  #screen coords, world coords. world converted to screen
            self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
            #print('world coordinates ' + str(self.boxx) + ', ' + str(self.boxy))
            #print('screen coordsinates ' + str(self.boxx - cameraBlocksX) + ', ' + str(self.boxy - cameraBlocksY))
            if self.state: # == True:
                self.drawBlock(WIREBLOCKON)
            else:
                self.drawBlock(WIREBLOCKOFF)
            

    def drawBlock(self, block): #cull (do not draw) blocks outside camera view
        #if self.onScreen:
            pygame.draw.rect(DISPLAYSURF, block, self.blockLocSize)  #screen coords
        #else:
            #self.blockLocSize = None

    def Output(self, queryingBlockX, queryingBlockY): #gives querying transistor the current state
        return self.state   


class TransistorBlock(Block):
    def __init__(self, type, boxx, boxy, inputSideX, inputSideY, outputSideX1, outputSideY1, outputSideX2, outputSideY2, outputSideX3, outputSideY3):  #screen coords
        self.boxx, self.boxy = (boxx + cameraBlocksX, boxy + cameraBlocksY) #world coords, screen coords. screen converted to world
        self.left, self.top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
        self.inputBlock = (inputSideX + self.boxx, inputSideY + self.boxy) #world coords
        self.outputBlock1 = (outputSideX1 + self.boxx, outputSideY1 + self.boxy) #world coords
        self.outputBlock2 = (outputSideX2 + self.boxx, outputSideY2 + self.boxy) #world coords
        self.outputBlock3 = (outputSideX3 + self.boxx, outputSideY3 + self.boxy) #world coords
        self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
        self.onScreen = True #set to false if block is outside camera view
        self.Operation() #set initial state by doing one operation
        #print('world coordinates ' + str(self.boxx) + ', ' + str(self.boxy))

    #def initialSetup(self):
    #    if self.inputBlock in mainDict: #check if input block exists
    #        self.state = not mainDict[self.inputBlock].Output(self.boxx, self.boxy)
    #        if self.state: # == True:
    #            pygame.draw.rect(DISPLAYSURF, TRANSISTORBLOCKON, self.blockLocSize)
    #        else:
    #            pygame.draw.rect(DISPLAYSURF, TRANSISTORBLOCKOFF, self.blockLocSize)
    #    else: #if no block exists at input turn transistor on
    #        self.state = ON
    #        pygame.draw.rect(DISPLAYSURF, TRANSISTORBLOCKON, self.blockLocSize)
    def Operation(self): #takes the inputs from surrounding blocks
        if self.inputBlock in mainDict: #check if input block exists
            self.state = not mainDict[self.inputBlock].Output(self.boxx, self.boxy) #world coords
            if self.state: # == True:
                if self.onScreen:
                    self.drawBlock(TRANSISTORBLOCKON)
            else:
                if self.onScreen:
                    self.drawBlock(TRANSISTORBLOCKOFF)
        else: #if no block exists at input turn transistor on
            self.state = ON
            if self.onScreen:
                self.drawBlock(TRANSISTORBLOCKON)
                #test to see if block is on screen
    #if it is draw it as empty in current location
    #test to see if block is still on the screen in its new location
    #if it is redraw at new location
    #--- OR ---
    #check onScreen bool to see if block is on screen
    #if it is draw it as empty in current location
    #update on screen bool by testing to see if block is still on screen in new location
    #and if it is on screen redraw at new location
    def repositionOnScreen(self): #screen coords
        if self.onScreen:
            self.left, self.top = leftTopCoordsOfBox(self.boxx - cameraBlocksX, self.boxy - cameraBlocksY)  #screen coords, world coords. world converted to screen
            self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
            #print('world coordinates ' + str(self.boxx) + ', ' + str(self.boxy))
            #print('screen coordsinates ' + str(self.boxx - cameraBlocksX) + ', ' + str(self.boxy - cameraBlocksY))
            if self.state: # == True:
                self.drawBlock(TRANSISTORBLOCKON)
            else:
                self.drawBlock(TRANSISTORBLOCKOFF)

    def drawBlock(self, block): 
       #if self.onScreen: #cull (do not draw) blocks outside camera view     
            pygame.draw.rect(DISPLAYSURF, block, self.blockLocSize)  #screen coords
        #else:
            #self.blockLocSize = None

    def returnConnectedUnprocessedWires(self):
        self.unprocessedWireList = []
        if self.outputBlock1 in wireSet: #check if block is a wire
            if not mainDict[self.outputBlock1].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.outputBlock1) #add wire to return list
        if self.outputBlock2 in wireSet: #check if block is a wire
            if not mainDict[self.outputBlock2].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.outputBlock2) #add wire to return list
        if self.outputBlock3 in wireSet: #check if block is a wire
            if not mainDict[self.outputBlock3].getProcessedThisTick(): #check if wire hasn't been processed
                self.unprocessedWireList.append(self.outputBlock3) #add wire to return list
        return self.unprocessedWireList

    def getState(self):
        return self.state 
    
    def Output(self, queryingBlockX, queryingBlockY): #gives querying transistor the current state
        if (queryingBlockX, queryingBlockY) == self.inputBlock:
            return OFF #always return off if querying transistor is input block
        else:
            return self.state   
 

          
def main():
    PROCESSRATE = 100 #process cycles at a set rate in milliseconds
    elapsedTime = 0 #ammount of time in milliseconds since late procress cycle

    global FPSCLOCK, DISPLAYSURF
    global selectedBlockType

    global cameraPixX, cameraPixY #current camera x,y
    cameraPixX = 0 #top left of current draw area, other end is board width, IN pixels
    cameraPixY = 0 #top left of current draw area, other end is board height

    global cameraBlocksX, cameraBlocksY
    global lastCameraX, lastCameraY #last camera x,y
    cameraBlocksX = 0 #top left of current draw area, other end is board width, IN Blocks
    cameraBlocksY = 0 #top left of current draw area, other end is board height
    lastCameraX = 0
    lastCameraY = 0



    selectedBlockType = 1

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
 
    currentWire = None #used for processing wires
    unprocessedWires = set()

    pygame.init()


    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render('FPS', True, YELLOW)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (33, 25)
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    boxx, boxy = 0, 0

    pygame.display.set_caption('Logic Simulator')

    pygame.draw.rect(DISPLAYSURF, BGCOLOR, GRIDBACKGROUND)
    
    drawEmptyBoard()

    while True: # main game loop    
        for event in pygame.event.get(): # event handling loop
            #(mouseLeft, mouseMiddle, mouseRight) = pygame.mouse.get_pressed() #poll mouse
            #print(event)
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_1:
                    selectedBlockType = 1
                    print ('selected wire blocks')
                elif event.key == K_2:
                    selectedBlockType = 2
                    print ('selected left transistor blocks')
                elif event.key == K_3:
                    selectedBlockType = 3
                    print ('selected right transistor blocks')
                elif event.key == K_4:
                    selectedBlockType = 4
                    print ('selected up transistor blocks')
                elif event.key == K_5:
                    selectedBlockType = 5
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
                        #print(relativePosition)
                        #print(abs(movementTotalX), abs(movementTotalY))
                    if relativePosition[0] < 0:
                        #print('moveing left')
                        totalLeft += abs(relativePosition[0])
                        totalRight = 0
                    if relativePosition[0] > 0:
                        #print('moveing right')
                        totalRight += abs(relativePosition[0])
                        totalLeft = 0
                    if relativePosition[1] < 0:
                        #print('moveing up')
                        totalUp += abs(relativePosition[1])
                        totalDown = 0
                    if relativePosition[1] > 0:
                        #print('moveing down')    
                        totalDown += abs(relativePosition[1])
                        totalUp = 0
                    #print('Left ' + str(totalLeft) + ' Right ' + str(totalRight))
                    #print('Up ' + str(totalUp) + ' Down ' + str(totalDown))
                    if totalLeft >= TOTALBOXSIZE:
                        cameraPixX += TOTALBOXSIZE
                        lastCameraX = cameraBlocksX
                        cameraBlocksX += 1
                        totalLeft = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalRight >= TOTALBOXSIZE:
                        cameraPixX -= TOTALBOXSIZE
                        lastCameraX = cameraBlocksX
                        cameraBlocksX -= 1
                        totalRight = 0
                        clearDrawArea()
                        moveBlocks()
                    if totalUp >= TOTALBOXSIZE:
                        cameraPixY += TOTALBOXSIZE
                        lastCameraY = cameraBlocksY
                        cameraBlocksY += 1
                        totalUp = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalDown >= TOTALBOXSIZE:
                        cameraPixY -= TOTALBOXSIZE
                        lastCameraY = cameraBlocksY
                        cameraBlocksY -= 1
                        totalDown = 0
                        clearDrawArea()
                        moveBlocks()
                    #print('current draw area pixels ' + str(cameraPixX) + ', ' + str(cameraPixY))
                    #print('current draw area blocks ' + str(cameraBlocksX) + ', ' + str(cameraBlocksY))
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    leftMouseDown = True
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
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
                    rightMouseDown = True
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                elif event.button == 4:
                    print('mouse wheel up')
                elif event.button == 5:
                    print('mouse wheel down')
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    leftMouseDown = False
                elif event.button == 2:
                    middleMouse = False
                    firstMoveMiddle = True
                elif event.button == 3:
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

            for operateTransistorKey in transistorSet:
                mainDict[operateTransistorKey].Operation()  
                
            #turn off every wire, then turn on only the wires that are comming on or staying on in this cycle that way we wont need to specifically turn off wires
            for turnOffWiresKey in wireSet:
                mainDict[turnOffWiresKey].turnOff()       
        
            #process wires here instead of in transistor objects
            for processWiresKey in transistorSet: #loop through all transistors
                if mainDict[processWiresKey].getState(): #check if current transistor is switched ON, if OFF skip
                
                    #ask current transistor to return list of connected wires that have not been processed this tick (add def to transistor and wire classes that filters these wires)
                    #add returned list to set/queue
                    for transistorWire in mainDict[processWiresKey].returnConnectedUnprocessedWires():
                        unprocessedWires.add(transistorWire)                 
                    #loop through each wire in set
                    while unprocessedWires: #while set/queue is not empty:
                        currentWire = unprocessedWires.pop()
                        mainDict[currentWire].turnOn() #turn on current wire setTick/processed-boolean
                        for wire in mainDict[currentWire].returnConnectedUnprocessedWires(): #ask current wire to return list of surrounding unprocessed wires and add to set
                            unprocessedWires.add(wire)
            #doDraws = True
        
        #draw only the blocks in the current draw area here
        #if doDraws == True:
        #    for drawWire in wireSet:
        #        draw = mainDict[drawWire].getDrawTuple()
        #        pygame.draw.rect(DISPLAYSURF, draw[0], draw[1])
        #    for drawTransistor in transistorSet:
        #        draw = mainDict[drawTransistor].getDrawTuple()
        #        pygame.draw.rect(DISPLAYSURF, draw[0], draw[1])
        #    doDraws = False
        #Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, 78, 36)) #remove last blitted FPS
        textSurfaceObj = fontObj.render('%.2f' % FPSCLOCK.get_fps(), True, YELLOW)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def leftTopCoordsOfBox(boxx, boxy):  #screen coords
    #Convert block coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN  #screen coords
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN  #screen coords
    return (left, top)  #screen coords


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
            #wireSet.add((boxx, boxy))
            #mainDict[boxx, boxy] = WireBlock(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE)) #screen coords


def clearDrawArea(): #only clear filled blocks not empty blocks, should be quicker than redrawing entire screen for every move
    for wire in wireSet: #world coords
        if (wire[0] >= cameraBlocksX and wire[0] <= cameraBlocksX + BOARDWIDTH - 1) and (wire[1] >= cameraBlocksY and wire[1] <= cameraBlocksY + BOARDHEIGHT - 1): #checks if block is on screen
            location = mainDict[wire].blockLocSize #screen coords
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCKBORDER, location) #clears yellow edge left from transistor, prevents haveing to redraw background
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (location[0] + 1, location[1] + 1, BOXSIZE, BOXSIZE)) #screen coords
            mainDict[wire].onScreen = True
            #print('----')
            #print('on screen')       
        else: #if block off screen
            location = mainDict[wire].blockLocSize #screen coords
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCKBORDER, location) #clears yellow edge left from transistor, prevents haveing to redraw background
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (location[0] + 1, location[1] + 1, BOXSIZE, BOXSIZE)) #screen coords
            mainDict[wire].onScreen = False
            #print('----')
            #print('off screen')            
    for transistor in transistorSet: #world coords
        if (transistor[0] >= cameraBlocksX and transistor[0] <= cameraBlocksX + BOARDWIDTH - 1) and (transistor[1] >= cameraBlocksY and transistor[1] <= cameraBlocksY + BOARDHEIGHT - 1):
            location = mainDict[transistor].blockLocSize #screen coords
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCKBORDER, location) #clears yellow edge left from transistor, prevents haveing to redraw background
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (location[0] + 1, location[1] + 1, BOXSIZE, BOXSIZE)) #screen coords
            mainDict[transistor].onScreen = True
            #print('----')
            #print('on screen')       
        else: #if block off screen
            location = mainDict[transistor].blockLocSize #screen coords
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCKBORDER, location) #clears yellow edge left from transistor, prevents haveing to redraw background
            pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (location[0] + 1, location[1] + 1, BOXSIZE, BOXSIZE)) #screen coords
            mainDict[transistor].onScreen = False
            #print('----')
            #print('off screen')            


def moveBlocks():
    for wire in wireSet: #world coords
        mainDict[wire].repositionOnScreen()
    for transistor in transistorSet: #world coords
        mainDict[transistor].repositionOnScreen()

def deleteBlock(boxx, boxy): #screen coords
    worldX, worldY = boxx + cameraBlocksX, boxy + cameraBlocksY
    if (worldX, worldY) in mainDict: #world coords
        if (worldX, worldY) in transistorSet: #world coords
            transistorSet.remove((worldX, worldY)) #world coords
        else:
            wireSet.remove((worldX, worldY)) #world coords
        del mainDict[worldX, worldY] #world coords
        left, top = leftTopCoordsOfBox(boxx, boxy) #screen coords
        pygame.draw.rect(DISPLAYSURF, EMPTYBLOCKBORDER, (left - 1, top - 1, TOTALBOXSIZE, TOTALBOXSIZE)) #clears yellow edge left from transistor, prevents haveing to redraw background
        pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE))
                                                         #^screen coords
#send in screen coords to block object constructors
def setBlock(boxx, boxy): #screen coords
    worldX, worldY = boxx + cameraBlocksX, boxy + cameraBlocksY
    if selectedBlockType == 1:
        if (worldX, worldY) not in mainDict:
            wireSet.add((worldX, worldY))
            mainDict[worldX, worldY] = WireBlock(boxx, boxy)
    elif selectedBlockType == 2: #left input transistor
        if (worldX, worldY) not in mainDict:
            transistorSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(LEFT, boxx, boxy, LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY)
    elif selectedBlockType == 3: #right input transistor
        if (worldX, worldY) not in mainDict: 
            transistorSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(RIGHT, boxx, boxy, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY)
    elif selectedBlockType == 4: #up input transistor
        if (worldX, worldY) not in mainDict: 
            transistorSet.add((worldX, worldY)) 
            mainDict[worldX, worldY] = TransistorBlock(UP, boxx, boxy, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY)
    elif selectedBlockType == 5: #down input transistor
        if (worldX, worldY) not in mainDict:
            transistorSet.add((worldX, worldY))
            mainDict[worldX, worldY] = TransistorBlock(DOWN, boxx, boxy, DOWNSIDEX, DOWNSIDEY, LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY)


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



