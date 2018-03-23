#Master Branch
import pygame, sys
from pygame.locals import *
from Consts import *
from Sto import *
from Display import *
from Globals import CameraBlocksX, CameraBlocksY, SelectedBlockType, BoxSize, BoardHeight, BoardWidth, leftTopCoordsOfBox, getBoxAtPixel
from WireBlock import WireBlock
from BlockEditDefs import setBlock, deleteBlock, mapWirePaths
from BlockMoveDefs import clearDrawArea, moveBlocks, zoomIn, zoomOut, zoomBlocks

         
def main():
    PROCESSRATE = 100 #process cycles at a set rate in milliseconds
    elapsedTime = 0 #ammount of time in milliseconds since last procress cycle

    leftMouseDown = False
    middleMouse = False
    rightMouseDown = False

    firstMoveMiddle = True #set false after initial move with middle mouse down

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

    #drawRect(BGCOLOR, GRIDBACKGROUND)
    drawBorder()
    
    #drawFullBoardTest()

    while True: # main game loop    
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_1:
                    SelectedBlockType.set(1)
                    print ('selected wire blocks')
                elif event.key == K_2:
                    SelectedBlockType.set(2)
                    print ('selected left transistor blocks')
                elif event.key == K_3:
                    SelectedBlockType.set(3)
                    print ('selected right transistor blocks')
                elif event.key == K_4:
                    SelectedBlockType.set(4)
                    print ('selected up transistor blocks')
                elif event.key == K_5:
                    SelectedBlockType.set(5)
                    print ('selected down transistor blocks')
                elif event.key == K_6:
                    pass
                    #print(getCtrBlockWorldCoords())                   
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
                    if totalLeft >= BoxSize.get():
                        #CameraBlocksX.setPix(CameraBlocksX.get() + totalLeft)
                        CameraBlocksX.inc()
                        totalLeft = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalRight >= BoxSize.get():
                        #CameraBlocksX.setPix(CameraBlocksX.get() - totalRight)
                        CameraBlocksX.dec()
                        totalRight = 0
                        clearDrawArea()
                        moveBlocks()
                    if totalUp >= BoxSize.get():
                        #CameraBlocksY.setPix(CameraBlocksY.get() + totalUp)
                        CameraBlocksY.inc()
                        totalUp = 0
                        clearDrawArea()
                        moveBlocks()
                    elif totalDown >= BoxSize.get():
                        #CameraBlocksY.setPix(CameraBlocksY.get() - totalDown)
                        CameraBlocksY.dec()
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
                    relativePosition = pygame.mouse.get_rel() #clears built up relative movements
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
                    clearDrawArea()
                    zoomIn()
                    zoomBlocks()
                elif event.button == 5:
                    clearDrawArea()
                    zoomOut()
                    zoomBlocks()
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
        drawFPSRect(BLACK, (0, 0, 78, 36)) #remove last blitted FPS
        textSurfaceObj = fontObj.render('%.2f' % FPSCLOCK.get_fps(), True, YELLOW)
        blitToSurf(textSurfaceObj, textRectObj)
        

def drawFullBoardTest(): #for testing performance only
    for boxx in range(BoardWidth.get()): #screen coords
        for boxy in range(BoardHeight.get()): #screen coords
            #boxx, boxy = 0, 0
            left, top = leftTopCoordsOfBox(boxx, boxy) #screen coords
            WSet.add((boxx, boxy))
            mainDict[boxx, boxy] = WireBlock(boxx, boxy)
            drawRect(WIREBLOCKOFF, (left, top, BoxSize.get(), BoxSize.get())) #screen coords
boxx, boxy = int(BoardWidth.get()/2), int((BoardHeight.get()-(TOPBAR / BoxSize.get()))/2)
print((boxx, boxy))
left, top = leftTopCoordsOfBox(boxx, boxy) #screen coords
WSet.add((boxx, boxy))
mainDict[boxx, boxy] = WireBlock(boxx, boxy)
mapWirePaths()
drawRect(WIREBLOCKOFF, (left, top, BoxSize.get(), BoxSize.get())) #screen coords
            
#def drawBoard(dict):
#    for boxx in xrange(BoardWidth.get()):
#        for boxy in xrange(BoardHeight.get()):
#            left, top = leftTopCoordsOfBox(boxx, boxy)
#            if type(board[boxx + 1, boxy + 1]) is EmptyBlock:
#                pygame.draw.rect(DISPLAYSURF, RED, (left - 1, top - 1, BoxSize.get() + 2, BoxSize.get() + 2), 1) #clears yellow edge left from transistor, prevents haveing to redraw background
#                pygame.draw.rect(DISPLAYSURF, EMPTYBLOCK, (left, top, BoxSize.get(), BoxSize.get()))
#            elif type(board[boxx + 1, boxy + 1]) is WireBlock:
#                pygame.draw.rect(DISPLAYSURF, WIREBLOCK, (left - 1, top - 1, BoxSize.get() + 2, BoxSize.get() + 2))
#            elif type(board[boxx + 1, boxy + 1]) is TransistorBlock:
#                pygame.draw.rect(DISPLAYSURF, TRANSISTORBLOCK, (left - 1, top - 1, BoxSize.get() + 2, BoxSize.get() + 2))

#def drawIcon(shape, color, boxx, boxy):
#    quarter = int(BoxSize.get() * 0.25) # syntactic sugar
#    half =    int(BoxSize.get() * 0.5)  # syntactic sugar

#    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
#    # Draw the shapes
#    if shape == SQUARE:
#        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BoxSize.get() - half, BoxSize.get() - half)) ##use for drawing wires and transistors

if __name__ == '__main__':
    main()



