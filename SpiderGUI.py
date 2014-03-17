import pygame, sys
import math
from pygame.locals import *
from SpiderStack import *
from SpiderDeck import *
from SpiderCard import *
from SpiderSolitaire import *


#Global constants
windowWidth = 1500
windowHeight = 850
cardWidth = 100
cardHeight = 132
hiddenGap = 10
revealedGap = 30
deck_x = 1300
deck_y = 650

#Global variables
x = []
m = 0
y = 20
hitboxes = []
stackhboxes = []
stacks = []
game = 0
inHand = SpiderStack([],0)




def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    global m
    global x
    
    m = (windowWidth-10*cardWidth)/11
    for i in range(0,10):
        x.append(i*cardWidth+(i+1)*m)
    
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(pygame.Color(100,200,100))
    initialize(spiderWindow,2)
    pygame.display.flip()
    
    updateHitboxes()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                loc = detectCol()
                print loc
                if not loc == (-1,-1):
                    pickupCards(loc)
            elif event.type == MOUSEMOTION:
                if not inHand.isEmpty():
                    print "I should be doing something!"
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    displayStack(spiderWindow,inHand,mouse_x,mouse_y)
                    
                
        
    pygame.display.update()
    fpsClock.tick(30)

def initialize(surface, suitNo):
    global game
    global stacks
    game = SpiderSolitaire(suitNo)
    stacks = game.getStacks()
    displayStacks(surface, stacks, x, y)
    displayDeck(surface)

def displayStacks(surface, Stacks, x, y):
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, Stacks[i], x[i], y)

def displayStack(surface, Stack, stack_x,stack_y):
    cards,hiddenNo = Stack.getStack()
    
    n = len(cards)
    print n
    gap = 0
    card_x,card_y = stack_x,stack_y
    for i in range(0,n):
        if(i < hiddenNo):
            isHidden=True
            gap = hiddenGap
        else:
            print "Found one!"
            isHidden=False
            gap = revealedGap 
        print "puttin a card at (%d,%d)"%(card_x,card_y)       
        displayCard(surface,cards[i],isHidden,card_x,card_y)
        card_y += gap
    pygame.display.update()
        

def displayCard(surface, card, isHidden, card_x,card_y):
    cardSurf = card.getImage(isHidden)
    cardSurf = pygame.transform.smoothscale(cardSurf,(cardWidth,cardHeight))
    surface.blit(cardSurf, (card_x,card_y))

def displayDeck(surface):
    C = SpiderCard('S',1)
    cardBack = C.getImage(True)
    cardBack = pygame.transform.smoothscale(cardBack, (cardWidth, cardHeight))
    for i in range(0,4):
        surface.blit(cardBack, (deck_x-i*hiddenGap,deck_y))
    return

def updateHitboxes():
    global hitboxes
    global stackhboxes
    hitboxes = []
    stackhboxes = []
    for i in range(0,len(stacks)):
        stack = stacks[i]
        cards = stack.getStack()[0]
        hitstack = []
        for j in range(0,len(cards)):
            card = cards[j]
            cardLoc = getCardLoc(i,j)
            hitbox = card.getImage().get_rect()
            hitbox = hitbox.move(cardLoc)
            hitstack.append(hitbox)
        hitboxes.append(hitstack)
        stackHeight = getCardLoc(i,len(cards)-1)[1]+cardHeight
        stackhbox = pygame.Rect(x[i],y+hiddenGap,cardWidth,stackHeight)
        stackhboxes.append(stackhbox)
    
def getCardLoc(i,j):
    hidden = stacks[i].getStack()[1]
    card_x = x[i]
    card_y = y
    if j <= hidden:
        card_y += j*hiddenGap
    else:
        card_y = hidden*hiddenGap+(j-hidden)*revealedGap
    return (card_x,card_y)

def detectCol():
    mouse = pygame.mouse.get_pos()
    for i in range(0,len(stackhboxes)):
        if not stackhboxes[i].collidepoint(mouse):
            continue
        for j in range(0,len(hitboxes[i])):
            h = -(j+1)
            if hitboxes[i][h].collidepoint(mouse):
                return (i,len(hitboxes[i])+h)
    return (-1,-1)

def pickupCards((i,j)):
    global inHand
    global stacks
    inHand = stacks[i].remove(len(stacks[i])-j)
    print len(inHand)
    print inHand.hasVisible()
    
    

if __name__ == '__main__':
    main()
     
pygame.quit()