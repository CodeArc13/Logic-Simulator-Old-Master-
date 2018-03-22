import pygame
from Consts import WINDOWWIDTH, WINDOWHEIGHT, BGCOLOR
from Globals import Border

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def drawRect(block, locAndSize):
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def drawFPSRect(block, locAndSize):
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def drawBorder():
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, Border.get(), 2)

def blitToSurf(surfObj, rectObj):
    DISPLAYSURF.blit(surfObj, rectObj)


