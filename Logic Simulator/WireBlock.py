from Block import *
from Display import drawRect
from Globals import CameraBlocksX, CameraBlocksY, EditCounter, BoxSize, BoardHeight, BoardWidth, leftTopCoordsOfBox
from Consts import WIREBLOCKOFF, WIREBLOCKON, RIGHTSIDEX, LEFTSIDEX, UPSIDEY, DOWNSIDEY, OFF
from Sto import mainDict, WSet


class WireBlock(Block):
    wireBlockDeleted = False
    def __init__(self, boxx, boxy): #screen coords
        self.boxx, self.boxy = (boxx + CameraBlocksX.get(), boxy + CameraBlocksY.get()) #world coords, screen coords. screen converted to world
        self.left, self.top = leftTopCoordsOfBox(boxx, boxy)  #screen coords
        self.inputBlockL = (LEFTSIDEX + self.boxx, self.boxy) #world coords
        self.inputBlockR = (RIGHTSIDEX + self.boxx, self.boxy) #world coords
        self.inputBlockU = (self.boxx, UPSIDEY + self.boxy) #world coords
        self.inputBlockD = (self.boxx, DOWNSIDEY + self.boxy) #world coords
        self.blockLocSize = (self.left, self.top, BoxSize.get(), BoxSize.get()) #screen coords
        self.onScreen = True
        self.processedThisTick = False
        self.state = OFF
        self.editCount = -1
        self.wirePathID = None #must be set in edit
        self.drawBlock()

    def setWireBlockDeleted(deleted):
        WireBlock.wireBlockDeleted = deleted      
        
    def getWireBlockDeleted():
        return WireBlock.wireBlockDeleted     
    
    def returnConnectedUneditedWires(self):
        self.uneditedWireList = []
        if self.inputBlockL in WSet: #check if block is a wire
            if mainDict[self.inputBlockL].getEditCount() < EditCounter.get(): #check if wire hasn't been edited this edit
                self.uneditedWireList.append(self.inputBlockL) #add wire to return list
        if self.inputBlockR in WSet: #check if block is a wire
            if mainDict[self.inputBlockR].getEditCount() < EditCounter.get(): #check if wire hasn't been edited this edit
                self.uneditedWireList.append(self.inputBlockR) #add wire to return list
        if self.inputBlockU in WSet: #check if block is a wire
            if mainDict[self.inputBlockU].getEditCount() < EditCounter.get(): #check if wire hasn't been edited this edit
                self.uneditedWireList.append(self.inputBlockU) #add wire to return list
        if self.inputBlockD in WSet: #check if block is a wire
            if mainDict[self.inputBlockD].getEditCount() < EditCounter.get(): #check if wire hasn't been edited this edit
                self.uneditedWireList.append(self.inputBlockD) #add wire to return list
        return self.uneditedWireList

    def getWirePathID(self):
        return self.wirePathID

    def setWirePathID(self, wirePathID):
        self.wirePathID = wirePathID

    def getEditCount(self):
        return self.editCount

    def setEditCount(self, editCount):
        self.editCount = editCount

    def switchWire(self, state):
        self.state = state
        if self.onScreen:
            self.drawBlock()   
            
    def getLocation(self):
        return (self.boxx, self.boxy)

    def repositionOnScreen(self): #screen coords
        if self.onScreen:
            self.left, self.top = leftTopCoordsOfBox(self.boxx - CameraBlocksX.get(), self.boxy - CameraBlocksY.get())  #screen coords, world coords. world converted to screen
            self.blockLocSize = (self.left, self.top, BoxSize.get(), BoxSize.get()) #screen coords
            self.drawBlock()      
            
    def drawBlock(self): #cull (do not draw) blocks outside camera view
        if self.state: #ON
            drawRect(WIREBLOCKON, self.blockLocSize)  #screen coords
        else: #OFF
            drawRect(WIREBLOCKOFF, self.blockLocSize) #screen coords

    def output(self, queryingBlockX, queryingBlockY): #gives querying transistor the current state
        return self.state   


