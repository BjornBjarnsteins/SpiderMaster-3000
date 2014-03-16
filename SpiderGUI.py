import pygame, sys
from pygame.locals import *

minredx,minredy = 100,100
maxredx,maxredy = 300,300
minbluex,minbluey = 700,100
maxbluex,maxbluey = 900,300
redx,redy = 120,120
bluex,bluey = 720,120
lastx,lasty = 0,0

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
       
        
        rectObj1 = pygame.Surface((200,200))
        rectObj2 = pygame.Surface((200,200))
        rectObj1.fill(pygame.Color(255,0,0))
        rectObj2.fill(pygame.Color(0,0,255))
        
        spiderWindow.blit(rectObj1, (100,100))
        spiderWindow.blit(rectObj2, (700,100))
        
        catObj = pygame.image.load('cat.jpg')
        catObj = pygame.transform.smoothscale(catObj, (170, 120))
        spiderWindow.blit(catObj,(picx,picy))
        
        pygame.display.flip()
        
        
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and inGrumpy(catObj):
                lastx,lasty = picx,picy
                picx,picy = pygame.mouse.get_pos()
                Holding = True
            elif event.type == MOUSEBUTTONUP and inGrumpy(catObj):
                if inBlue():
                    picx,picy = bluex,bluey
                elif inRed():
                    picx,picy = redx,redy
                else:
                    picx,picy = lastx,lasty
                Holding = False
            elif event.type == MOUSEMOTION and Holding and inGrumpy(catObj):
                picx,picy = pygame.mouse.get_pos()
                
        
    pygame.display.update()
    fpsClock.tick(30)

def inRed():
    x,y = pygame.mouse.get_pos()
    if x > minredx and x < maxredx and y > minredy and y < maxredy:
        return True
    else:
        return False
    
def inBlue():
    x,y = pygame.mouse.get_pos()
    if x > minbluex and x < maxbluex and y > minbluey and y < maxbluey:
        return True
    else:
        return False

def inGrumpy(surface):
    if surface.get_rect().collidepoint(pygame.mouse.get_pos()):
        return True
    else:
        return False

if __name__ == '__main__':
     main()