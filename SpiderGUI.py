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
pile_x = 30
pile_y = 650
NoSuits = 1
colNum = 10
deal = 4
cardBack = pygame.Surface((0,0))

aces = []


piles = []

#Global variables
x = []
m = 0
y = 20
hitboxes = [0]*colNum
stackhboxes = [0]*colNum
stackHeight = [0]*colNum
deckhboxes = [0]*deal
stacks = []
game = 0
inHand = SpiderStack([],0)
inHandSurf = pygame.Surface((0,0))
inHandRect = pygame.Rect(0,0,0,0)
backgroundColor = pygame.Color(100,200,100)
last_i,last_j = 0,0
mouseDown = False
mouse = (0,0)
background = 0


def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    global m
    global x
    global mouseDown
    global background
    global cardBack
    global aces
    
    m = (windowWidth-10*cardWidth)/11
    for i in range(0,10):
        x.append(i*cardWidth+(i+1)*m)
    
    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('SpiderSolitaire')
    spiderWindow.fill(backgroundColor)
    cardBack = SpiderCard('S',1).getImage(True)
    cardBack = pygame.transform.smoothscale(cardBack, (cardWidth, cardHeight))
    initialize(spiderWindow,NoSuits)
    for i in ['C','D','H','S']:
        cardSurface = SpiderCard(i,1).getImage()
        cardSurface = pygame.transform.smoothscale(cardSurface, (cardWidth, cardHeight))
        aces.append(cardSurface)
    
    displayPiles(spiderWindow)
    
    updateHitboxes()
    background = spiderWindow.copy()
    
    pygame.display.flip()
        
    while True:

        if not inHand.isEmpty() and mouseDown:
            spiderWindow.blit(background, (0,0))
            spiderWindow.blit(inHandSurf, mouse)
            pygame.display.update()
        
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
                        updateStack(spiderWindow, loc_i)
                        updateHitbox(loc_i)
                    else:
                        putdownCards(last_i)
                        updateStack(spiderWindow, last_i)
                elif not (loc_i,loc_j) == (-1,-1):
                    #displayStackHitboxes(spiderWindow)
                    if not stacks[loc_i].hasVisible():
                        stacks[loc_i].flip()
                    elif game.isLegalPickup(stacks[loc_i], loc_j): 
                        pickupCards(spiderWindow,(loc_i,loc_j)) #deletes from stack
                    else: 
                        print 'You cant do this'
                    updateStack(spiderWindow, loc_i) 
                    background = spiderWindow.copy()      
            elif event.type == MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
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
                        if checkPile(loc_i):
                            addToPiles(loc_i)
                            spiderWindow.blit(background, (0,0))
                            displayPiles(spiderWindow) 
                            updateStack(spiderWindow, loc_i)
                            updateHitbox(loc_i)
                        else:
                            updateHitbox(loc_i)
                            spiderWindow.blit(background, (0,0)) 
                            updateStack(spiderWindow, loc_i)
                    else:
                        putdownCards(last_i)
                        updateHitbox(loc_i)
                        spiderWindow.blit(background, (0,0))
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
    pygame.display.update()

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
        

def displayCard(surface, card, isHidden, card_x,card_y):
    cardSurf = card.getImage(isHidden)
    cardSurf = pygame.transform.smoothscale(cardSurf,(cardWidth,cardHeight))
    surface.blit(cardSurf, (card_x,card_y))

def displayDeck(surface):
    for i in range(0,deal):
        surface.blit(cardBack, (deck_x-i*hiddenGap,deck_y))
    return

def updateStack(surface, i):
    top_x,top_y = getCardLoc(i,0) #loc of top card so we can display Stack in same place
    stack = stacks[i]
    StackBox = stackhboxes[i]
    surface.fill(backgroundColor, StackBox)
    displayStack(surface,stack,top_x,top_y)
    pygame.display.update() 

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
    global stackHeight

    stack = stacks[i]
    cards = stack.getStack()[0]
    hitstack = []
    
    for j in range(0,len(cards)):
        cardLoc = getCardLoc(i,j)
        hitbox = pygame.Rect(cardLoc[0],cardLoc[1],cardWidth,cardHeight)
        hitstack.append(hitbox)
    hitboxes[i] = hitstack
    stackHeight[i] = getCardLoc(i,len(cards)-1)[1]+cardHeight
    stackhbox = pygame.Rect(x[i],y,cardWidth,stackHeight[i])
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
    
def updateInHandPos(surface):
    background = surface.copy()

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

def pickupCards(surface,(i,j)):
    global inHand
    global inHandSurf
    global stacks
    global last_i,last_j
    card_x,card_y = getCardLoc(i,j)
    toCopy = pygame.Rect(card_x,card_y,cardWidth,stackHeight[i]-card_y)
    inHandSurf = surface.subsurface(toCopy).copy()
    inHand = stacks[i].remove(len(stacks[i])-j)
    last_i = i
    last_j = j
    
def putdownCards(i):
    global inHand
    global stacks
    stacks[i].add(inHand)
    clearHand()
    
def clearHand():
    global inHand
    global inHandSurf
    inHand = SpiderStack([],0)
    inHandSurf = pygame.Surface((0,0))
    
def checkPile(i):
    if stacks[i].cards[-1].rank != 1 or len(stacks[i])<13:
        return False
    return game.inSuit(stacks[i], 13)

def addToPiles(i):
    global piles
    piles.append(stacks[i].remove(13).cards[-1].getSuitNo())
    
def displayPiles(surface):
    if len(piles) == 0:
        return
    for i in range(0,len(piles)):
        surface.blit(aces[piles[i]],(pile_x+i*revealedGap,pile_y))
    

if __name__ == '__main__':
    main()
     
pygame.quit()