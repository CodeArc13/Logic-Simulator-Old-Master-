from Block import *
from Display import drawRect
from Globals import CameraBlocksX, CameraBlocksY, leftTopCoordsOfBox
from Const import TOTALBOXSIZE, TRANSISTORBLOCKOFF, TRANSISTORBLOCKON, ON, OFF
from Sto import mainDict, WSet


class TransistorBlock(Block):
    def __init__(self, type, boxx, boxy, inputSideX, inputSideY, outputSideX1, outputSideY1, outputSideX2, outputSideY2, outputSideX3, outputSideY3):  #screen coords
        self.boxx, self.boxy = (boxx + CameraBlocksX.getX(), boxy + CameraBlocksY.getY()) #world coords, screen coords. screen converted to world
        self.left, self.top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
        self.inputBlock = (inputSideX + self.boxx, inputSideY + self.boxy) #world coords
        self.outputBlock1 = (outputSideX1 + self.boxx, outputSideY1 + self.boxy) #world coords
        self.outputBlock2 = (outputSideX2 + self.boxx, outputSideY2 + self.boxy) #world coords
        self.outputBlock3 = (outputSideX3 + self.boxx, outputSideY3 + self.boxy) #world coords
        self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
        self.onScreen = True #set to false if block is outside camera view
        self.previousState = None
        self.state = OFF
        self.wirePathIDs = set()

    def Operation(self): #takes the output from input block
        if self.inputBlock in mainDict: #check if input block exists
            self.state = not mainDict[self.inputBlock].output(self.boxx, self.boxy) #world coords
            if self.state != self.previousState: #if new state is the same as the previous state do nothing
                if self.onScreen:    
                    if self.state: # == True:               
                        self.drawBlock(TRANSISTORBLOCKON)
                    else:
                        self.drawBlock(TRANSISTORBLOCKOFF)
                self.previousState = self.state
        else: #if no block exists at input turn transistor ON
            if self.state == OFF: #only turn ON if transistor wasn't already ON
                self.state = ON
                if self.onScreen:
                    self.drawBlock(TRANSISTORBLOCKON)
                self.previousState = ON

    def clearWirePathIDs(self):
        self.wirePathIDs.clear()

    def addWirePathID(self, wirePathID):
        self.wirePathIDs.add(wirePathID)    
        
    def getWirePaths(self):
        return self.wirePathIDs

    def returnConnectedWires(self):
        self.connectedWireList = []
        if self.outputBlock1 in WSet: #check if block is a wire
            self.connectedWireList.append(self.outputBlock1) #add wire to return list
        if self.outputBlock2 in WSet: #check if block is a wire
            self.connectedWireList.append(self.outputBlock2) #add wire to return list
        if self.outputBlock3 in WSet: #check if block is a wire
            self.connectedWireList.append(self.outputBlock3) #add wire to return list
        return self.connectedWireList

    def getState(self):
        return self.state   

    def repositionOnScreen(self): #screen coords
        if self.onScreen:
            self.left, self.top = leftTopCoordsOfBox(self.boxx - CameraBlocksX.getX(), self.boxy - CameraBlocksY.getY())  #screen coords, world coords. world converted to screen
            self.blockLocSize = (self.left - 1, self.top - 1, TOTALBOXSIZE, TOTALBOXSIZE) #screen coords
            if self.state: # == True:
                self.drawBlock(TRANSISTORBLOCKON)
            else:
                self.drawBlock(TRANSISTORBLOCKOFF)

    def drawBlock(self, block): 
        drawRect(block, self.blockLocSize)  #screen coords
    
    def output(self, queryingBlockX, queryingBlockY): #gives querying transistor the current state
        if (queryingBlockX, queryingBlockY) == self.inputBlock:
            return OFF #always return off if querying transistor is input block
        else:
            return self.state   


