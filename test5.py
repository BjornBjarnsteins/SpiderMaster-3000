import pygame, sys
import math
from pygame.locals import *
from SpiderStack import *
from SpiderDeck import *
from SpiderCard import *
from SpiderSolitaire import *


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    windowWidth = 1500
    windowHeight = 850
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight), RESIZABLE)
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(pygame.Color(100,200,100))
    C = SpiderCard('C',10).getImage(False)
    x,y = 100,100
    #spiderWindow.blit(C, (x,y))
    pygame.display.flip()
    #C = pygame.image.load('cat.jpg')
    C = SpiderCard('C',10).getImage()
    
    while True:
        spiderWindow.fill(pygame.Color(100,200,100))
        spiderWindow.blit(C, (x,y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
            elif event.type == MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
                        
    pygame.display.update()
    fpsClock.tick(30)

                
                
if __name__ == '__main__':
    main()
     
pygame.quit()