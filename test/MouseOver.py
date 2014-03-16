import pygame, sys
from pygame.locals import *

def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    spiderWindow = pygame.display.set_mode((1000,800))
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(pygame.Color(55,200,70))
    color = pygame.Color(255,0,0)
    rectX, rectY, x, y = 100,100,0,0
    
    fullscreen = False
    
    while True:
        
        
        spiderWindow.fill(pygame.Color(55,200,70))
        rectObj = pygame.Surface((200,200))
        rectObj.fill(color)
        
        spiderWindow.blit(rectObj, (rectX,rectY))
        
        pygame.display.flip()
        
        
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
                collisionBox = rectObj.get_rect()
                collisionBox = collisionBox.move(rectX,rectY)
                if collisionBox.collidepoint(x,y):
                    color = pygame.Color(0,0,255)
                else:   
                    color = pygame.Color(255,0,0)
            elif event.type == KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        pygame.display.set_mode((1000,800),pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((1000,800))
                if event.key == K_ESCAPE:
                    fullscreen = False
                    pygame.display.set_mode((1000,800))
                        
                
        
    pygame.display.update()
    fpsClock.tick(30)

if __name__ == '__main__':
     main()