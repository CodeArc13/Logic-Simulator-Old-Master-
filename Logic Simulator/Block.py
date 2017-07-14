class Block(object): #base class of all block objects (abstract class of a sort)
    def __init__(self, boxx, boxy):
        pass

    def repositionOnScreen(self): #screen coords
        pass

    def drawBlock(self):
        pass

    def output(self, queryingBlockX, queryingBlockY): #gives querying block the current state
        pass