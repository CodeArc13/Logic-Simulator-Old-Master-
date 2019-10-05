import pygame
from Consts import WINDOWWIDTH, WINDOWHEIGHT, BGCOLOR, BLACK, GREEN
from Globals import Border, Xmargin, Ymargin

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#boardRect = (Xmargin.get(), Ymargin.get(), WINDOWWIDTH, WINDOWHEIGHT - Ymargin.get())
#boardRect = pygame.Rect(Xmargin.get(), Ymargin.get(), WINDOWWIDTH, WINDOWHEIGHT - Ymargin.get())

#def drawBoard():
#    pygame.draw.rect(DISPLAYSURF, BLACK, boardRect)

def drawRect(block, locAndSize):
    #boardRect.union_ip(pygame.Rect(block, locAndSize))
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def drawFPSRect(block, locAndSize):
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def drawBorder():
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, Border.get(), 2)

def blitToSurf(surfObj, rectObj):
    DISPLAYSURF.blit(surfObj, rectObj)


