from Consts import OFF, ON
from Sto import mainDict


class WirePath(object):
    currentWirePathID = 0 #current wirePathID being mapped in an edit
    def __init__(self, ID):
        self.pathSet = set()
        self.previousState = None
        self.state = OFF
        self.wirePathID = ID
        self.connectedTransistors = set() #number of connected transistors (only connected by outputs and not more than one entry per transistor i.e a set)
        
    def incrementCurrentWirePathID():
        WirePath.currentWirePathID += 1
        
    def resetWirePathID():
        WirePath.currentWirePathID = 0
        
    def addToPath(self, wireLoc):
        self.pathSet.add(wireLoc)

    def switchPath(self, state):
        self.state = state
        if self.state != self.previousState:
            for wire in self.pathSet:
                mainDict[wire].switchWire(self.state)
        self.previousState = self.state

    def turnOff(self):
        if self.state == ON: #only turn OFF if path ON - saves the loop if already OFF
            self.state = OFF
            for wire in self.pathSet:
                mainDict[wire].switchWire(OFF)

    def processWirePath(self):
        for transistor in self.connectedTransistors:
            if mainDict[transistor].getState() == ON:
                self.switchPath(ON)
                break
            self.switchPath(OFF) #if no connected transistors are ON then turn OFF path

    def getState(self):
        return (self.state)

    def addTrans(self, transLoc):
        self.connectedTransistors.add(transLoc)

    def remTrans(self, transLoc):
        self.connectedTransistors.remove(transLoc)

    def getTransTotal(self):
        return(len(self.connectedTransistors))


