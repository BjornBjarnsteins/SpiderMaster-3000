import pygame, sys
import math
from pygame.locals import *
from SpiderStack import *
from SpiderDeck import *
from SpiderCard import *
from SpiderSolitaire import *

windowWidth = 1500
windowHeight = 850
cardWidth = 100
cardHeight = 132
hiddenGap = 10
revealedGap = 30
x = []
m = (windowWidth-10*cardWidth)/11
for i in range(0,10):
    x.append(i*cardWidth+(i+1)*m)
y = 0


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight), RESIZABLE)
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(pygame.Color(100,200,100))
    initialize(spiderWindow,2)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
                
        
    pygame.display.update()
    fpsClock.tick(30)

def initialize(surface, suitNo):
    game = SpiderSolitaire(suitNo)
    game.deal()
    game.deal()
    game.deal()
    stacks = game.getStacks()
    displayStacks(surface, stacks, x, y)

def displayStacks(surface, Stacks, x, y):
    
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, Stacks[i], x[i], y)

def displayStack(surface, Stack, stack_x,stack_y):
    stack,hiddenNo = Stack.getStack()
    
    n = len(stack)
    gap = 0
    card_x,card_y = stack_x,stack_y
    for i in range(0,n):
        if(i <= hiddenNo):
            isHidden=True
            gap = hiddenGap
        elif(i == hiddenNo+1):
            isHidden=False
            gap = hiddenGap
        else:
            isHidden=False
            gap = revealedGap
            
        card_y += gap     
        displayCard(surface,stack[i],isHidden,card_x,card_y) 
        

def displayCard(surface, card, isHidden, card_x,card_y):
    cardSurf = card.getImage(isHidden)
    cardSurf = pygame.transform.smoothscale(cardSurf,(cardWidth,cardHeight))
    surface.blit(cardSurf, (card_x,card_y))

def displayDeck():
    return

if __name__ == '__main__':
    main()
     
pygame.quit()