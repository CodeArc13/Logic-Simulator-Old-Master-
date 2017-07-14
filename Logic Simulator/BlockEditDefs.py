from Sto import *
from Globals import SelectedBlockType, CameraBlocksX, CameraBlocksY, EditCounter, leftTopCoordsOfBox
from Display import drawRect
from Const import LEFTSIDEX, LEFTSIDEY, UPSIDEX, UPSIDEY, RIGHTSIDEX, RIGHTSIDEY, DOWNSIDEX, DOWNSIDEY, \
    LEFT, RIGHT, UP, DOWN, TOTALBOXSIZE, BOXSIZE, EMPTYBLOCKBORDER, EMPTYBLOCK
from WirePath import WirePath
from WireBlock import WireBlock
from TransistorBlock import TransistorBlock


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
        #drawRect(EMPTYBLOCKBORDER, (left - 1, top - 1, TOTALBOXSIZE, TOTALBOXSIZE)) #clears yellow edge left from transistor, prevents haveing to redraw background
        drawRect(EMPTYBLOCK, (left, top, BOXSIZE, BOXSIZE))
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
