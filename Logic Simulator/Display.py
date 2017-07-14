import pygame
from Const import WINDOWWIDTH, WINDOWHEIGHT, BGCOLOR, GRIDBACKGROUND


DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def drawRect(block, locAndSize):
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def drawBorder():
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, GRIDBACKGROUND, 2)

def blitToSurf(surfObj, rectObj):
    DISPLAYSURF.blit(surfObj, rectObj)


