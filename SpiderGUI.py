import pygame, sys
import math
from pygame.locals import *
from SpiderStack import *
from SpiderDeck import *
from SpiderCard import *
from SpiderSolitaire import *

windowWidth = 1500
windowHeight = 850
cardWidth = 150
cardHeight = 250
hiddenGap = 10
revealedGap = 30

def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight), RESIZABLE)
    pygame.display.set_caption('SpiderSolitaire')
    
    while True:
        spiderWindow.fill(pygame.Color(100,200,100))
        initialize(spiderWindow,2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
                
        
    pygame.display.update()
    fpsClock.tick(30)

def initialize(surface, suitNo):
    game = SpiderSolitaire(suitNo)
    game.deal()
    stacks = game.getStacks()
    displayStack(surface, stacks[0], 0,0)

def displayStacks(surface, Stacks, x, y):
    
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, Stacks[i], x[i], y[i])

def displayStack(surface, Stack, stack_x,stack_y):
    stack,hiddenNo = Stack.getStack()
    count = 0
    n = len(stack)
    gap = 0
    card_x,card_y = stack_x,stack_y
    for i in range(0,n):
        if(count < hiddenNo):
            isHidden=True
            gap = hiddenGap
        else:
            isHidden=False
            gap = revealedGap
            
        card_y += gap     
        displayCard(surface,stack[i],isHidden,card_x,card_y) 
        

def displayCard(surface, card, isHidden, stack_x,card_y):
    surface.blit(card.getImage(isHidden), (card_x,card_y))

def displayDeck():
    return
    

if __name__ == '__main__':
    main()
     
pygame.quit()