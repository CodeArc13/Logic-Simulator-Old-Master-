#Global Constants
FPS = 60 # frames per second, the general speed of the program
WINDOWWIDTH = 1000 # size of window's width in pixels
WINDOWHEIGHT = 1050 # size of windows' height in pixels
TOPBAR = 50
#BOARDHEIGHTPIX = BoardHeight.get() * BoxSize.get()
#BOARDWIDTHPIX = BoardWidth.get() * BoxSize.get() 

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