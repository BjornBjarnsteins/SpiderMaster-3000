import pygame, sys
from pygame.locals import *


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    spiderWindow = pygame.display.set_mode((1000,800))
    pygame.display.set_caption('SpiderSolitaire')
    
    
    
    mousex,mousey = 0,0
    picx, picy = 120,120
    Holding= False
    
    while True:
        spiderWindow.fill(pygame.Color(55,200,70))
        catObj = pygame.image.load('cat.jpg')
        catObj = pygame.transform.smoothscale(catObj, (290, 220))
        spiderWindow.blit(catObj,(picx,picy))
        grumpyRect = catObj.get_rect()
        grumpyRect = grumpyRect.move(picx,picy)
        if grumpyRect.collidepoint(pygame.mouse.get_pos()):
            #catObj = pygame.Surface((70,20))
            #catObj.fill(pygame.Color(255,0,0))
            boobies = pygame.image.load('boobs.jpg')
            boobies = pygame.transform.smoothscale(boobies, (95,70))
            spiderWindow.blit(catObj,(picx,picy))
            spiderWindow.blit(boobies,(picx+120,picy+150))
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        fpsClock.tick(30)
    
if __name__ == '__main__':
     main()