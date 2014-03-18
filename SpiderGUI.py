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
NoSuits = 2
colNum = 10
deal = 4

#Global variables
x = []
m = 0
y = 20
hitboxes = [0]*colNum
stackhboxes = [0]*colNum
deckhboxes = [0]*deal
stacks = []
game = 0
inHand = SpiderStack([],0)
backgroundColor = pygame.Color(100,200,100)
last_i,last_j = 0,0
mouseDown = False


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    global m
    global x
    global mouseDown
    
    m = (windowWidth-10*cardWidth)/11
    for i in range(0,10):
        x.append(i*cardWidth+(i+1)*m)
    
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(backgroundColor)
    initialize(spiderWindow,NoSuits)
    pygame.display.flip()
    
    updateHitboxes()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseDown = True
                updateHitboxes()
                loc_i,loc_j = detectCol()
                
                if deal != 0 and detectDeckCol():
                    dealNew(spiderWindow)
                    updateDeck(spiderWindow)
                elif (loc_i,loc_j) == (-1,-1) and inHand.isEmpty():
                    continue      
                elif not inHand.isEmpty():
                    n = len(inHand)
                    if (loc_i,loc_j) != (-1,-1) and game.isLegalMove(inHand,stacks[loc_i]):
                        putdownCards(loc_i)
                        clearHand() 
                        updateStack(spiderWindow, loc_i)
                        updateHitbox(loc_i)
                    else:
                        putdownCards(last_i)
                        clearHand() 
                        updateStack(spiderWindow, last_i)
                elif not (loc_i,loc_j) == (-1,-1):
                    #displayStackHitboxes(spiderWindow)
                    if not stacks[loc_i].hasVisible():
                        stacks[loc_i].flip()
                    elif game.isLegalPickup(stacks[loc_i], loc_j): 
                        pickupCards((loc_i,loc_j)) #deletes from stack
                    else: 
                        print 'You cant do this'
                    updateStack(spiderWindow, loc_i)       
            elif event.type == MOUSEMOTION and mouseDown:
                if not inHand.isEmpty():
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    temp = pygame.Surface.copy(spiderWindow)
                    displayStack(spiderWindow,inHand,mouse_x,mouse_y)
                    spiderWindow.blit(temp, (0,0))
            elif event.type == MOUSEBUTTONUP:
                mouseDown = False
                updateHitboxes()
                loc_i,loc_j = detectCol()
                
                if (loc_i,loc_j) == (-1,-1) and inHand.isEmpty():
                    continue      
                elif not inHand.isEmpty():
                    n = len(inHand)
                    if (loc_i,loc_j) != (-1,-1) and game.isLegalMove(inHand,stacks[loc_i]):
                        putdownCards(loc_i)
                        clearHand()
                        updateHitbox(loc_i) 
                        updateStack(spiderWindow, loc_i)
                    else:
                        putdownCards(last_i)
                        clearHand()
                        updateHitbox(loc_i)
                        updateStack(spiderWindow, last_i)
                
                

    #updateBox = pygame.Rect(mouse_x,mouse_y,-cardWidth,-cardHeight)
    #updateBox.fill(backgroundColor)    
    pygame.display.update()
    fpsClock.tick(30)

def initialize(surface, suitNo):
    global game
    global stacks
    global deal
    game = SpiderSolitaire(suitNo)
    stacks = game.getStacks()
    deal = 4
    displayStacks(surface, stacks, x, y)
    displayDeck(surface)

def displayStacks(surface, Stacks, x, y):
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, Stacks[i], x[i], y)

def displayStack(surface, Stack, stack_x,stack_y):
    cards,hiddenNo = Stack.getStack()
    
    n = len(cards)
    gap = 0
    card_x,card_y = stack_x,stack_y
    for i in range(0,n):
        if(i < hiddenNo):
            isHidden=True
            gap = hiddenGap
        else:
            isHidden=False
            gap = revealedGap     
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
    for i in range(0,deal):
        surface.blit(cardBack, (deck_x-i*hiddenGap,deck_y))
    return

def updateStack(surface, i):
    top_x,top_y = getCardLoc(i,0) #loc of top card so we can display Stack in same place
    stack = stacks[i]
    StackBox = stackhboxes[i]
    surface.fill(backgroundColor, StackBox)
    pygame.display.update(StackBox) 
    displayStack(surface,stack,top_x,top_y)

def updateStacks(surface):
    for i in range(0,len(stacks)):
        updateHitbox(i)
        updateStack(surface, i)
    
def updateHitboxes():
    for i in range(0,colNum):
        updateHitbox(i)
        
def updateHitbox(i):
    global hitboxes
    global stackhboxes

    stack = stacks[i]
    cards = stack.getStack()[0]
    hitstack = []
    
    for j in range(0,len(cards)):
        card = cards[j]
        cardLoc = getCardLoc(i,j)
        hitbox = pygame.Rect(cardLoc[0],cardLoc[1],cardWidth,cardHeight)
        hitstack.append(hitbox)
    hitboxes[i] = hitstack
    stackHeight = getCardLoc(i,len(cards)-1)[1]+cardHeight
    stackhbox = pygame.Rect(x[i],y,cardWidth,stackHeight)
    stackhboxes[i] = stackhbox
    
#TESTING FALL
def displayStackHitboxes(surface):
    black = pygame.Color(0,0,0)
    for hitbox in stackhboxes:
        pygame.draw.rect(surface, black, hitbox, 2)
    

def updateDeckHitbox():
    global deckhboxes
    
    for i in range(0,deal):
        deckBox = pygame.Rect(deck_x-i*hiddenGap,deck_y, cardWidth, cardHeight)
        deckhboxes[i] = deckBox

def updateDeck(surface):
    updateDeckHitbox()
    deckBox = pygame.Rect(deck_x-deal*hiddenGap, deck_y, cardWidth+deal*hiddenGap, cardHeight)
    surface.fill(backgroundColor, deckBox)
    displayDeck(surface)
    pygame.display.update(deckBox) 

def dealNew(surface):
    global game
    global deal
    
    if(deal > 0):
        game.deal()
        updateHitboxes()
        updateStacks(surface)
        updateDeckHitbox()
        updateDeck(surface)
        deal -= 1
    else:
        print 'You cant deal another'
        
    
    
def getCardLoc(i,j):
    hidden = stacks[i].getStack()[1]
    card_x = x[i]
    card_y = y
    if j <= hidden:
        card_y += j*hiddenGap
    else:
        card_y = (hidden-1)*hiddenGap+((j+1)-hidden)*revealedGap
    return (card_x,card_y)

def detectCol():
    mouse = pygame.mouse.get_pos()
    for i in range(0,len(stackhboxes)):
        if not stackhboxes[i].collidepoint(mouse):
            continue
        for j in range(0,len(hitboxes[i])):
            h = -(j+1)
            h = len(hitboxes[i])+h
            if hitboxes[i][h].collidepoint(mouse):
                return (i,h)
        
    return (-1,-1)

def detectDeckCol():
    mouse = pygame.mouse.get_pos()
    updateDeckHitbox()
    return deckhboxes[-1].collidepoint(mouse)

def pickupCards((i,j)):
    global inHand
    global stacks
    global last_i,last_j
    inHand = stacks[i].remove(len(stacks[i])-j)
    last_i = i
    last_j = j
    
def putdownCards(i):
    global inHand
    global stacks
    stacks[i].add(inHand)
    
def clearHand():
    global inHand
    inHand = SpiderStack([],0) 

if __name__ == '__main__':
    main()
     
pygame.quit()