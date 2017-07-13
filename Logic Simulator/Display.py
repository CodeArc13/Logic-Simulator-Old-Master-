import pygame
from Const import WINDOWWIDTH, WINDOWHEIGHT


DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def drawRect(block, locAndSize):
    pygame.draw.rect(DISPLAYSURF, block, locAndSize)

def blitToSurf(surfObj, rectObj):
    DISPLAYSURF.blit(surfObj, rectObj)


