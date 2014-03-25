import pygame, sys
import math
from pygame import USEREVENT
from pygame.locals import *
from SpiderStack import *
from SpiderDeck import *
from SpiderCard import *
from SpiderSolitaire import *
from win32api import GetSystemMetrics
from HighscoreGUI import *

#Global constants
#Note: If fullscreen and/or resizable will be implemented, some of these will not be kept constant.
#screen dimensions:
systemWidth = GetSystemMetrics(0)
systemHeight = GetSystemMetrics(1)
windowWidth = min(systemWidth, 1500)
windowHeight = min(systemHeight, 850)
#windowWidth = 1500
#windowHeight = 850

#card dimensions
cardWidth = 100
cardHeight = 132
#number of suits in play:
NoSuits = 1
#gap settings
hiddenGap = 10 #the gap from a hidden card to the next card on top.
revealedGap = 30 #the gap from a revealed card to the next card on top.
#Coordinates of the deck.
deck_x = windowWidth - 200
deck_y = windowHeight - 200
#Coordinates of the full suits (='a pile') the user has collected.
pile_x = 30
pile_y = windowHeight - 200
#Coordinates of the timer
timer_x = windowWidth - 200
timer_y = windowHeight - 50
#Coordinates of the score
score_x = windowWidth - 500
score_y = windowHeight - 50
#number of stacks in game:
colNum = 10
#image of the back of a card
cardBack = pygame.Surface((0,0))
#surfaces for the aces:
aces = []

#Global variables
#Coordinates for the stack stacks[i] will be (x[i],y)
x = []
y = 20
#space between stacks
m = 0
#number of deals left:
deal = 5
#hitboxes for:
hitboxes = [0]*colNum #for the cards in game
stackhboxes = [0]*colNum #for the stacks
deckhboxes = [0]*deal #for the deal buttons
#variables for the stacks:
stackHeight = [0]*colNum
stacks = []
#this instance of spider solitaire:
game = 0
#contains collected piles denoted by suit number.
piles = []
#cards that have been picked up:
inHand = SpiderStack([],0)
inHandSurf = pygame.Surface((0,0)) #the image of inHand
inHandRect = pygame.Rect(0,0,0,0) #hitbox
#the fabulous green:
backgroundColor = pygame.Color(30,148,45)
#position where inHand was picked up last:
last_i,last_j = 0,0
mouseDown = False
mouse = (0,0)
#offset of the mouse and inHand, used for drawing
offset = (0,0)
#image to update the background while moving cards:
background = 0
mainBack = pygame.image.load('Backgrounds\grumpy_background.jpg')
#for help on/off:
helpOn = False
#for the help itself:
helpScreen = 0
fullscreenOn = False

# Initializes the game timer
time = 0
SEC_EVENT = USEREVENT + 1
pygame.time.set_timer(SEC_EVENT, 1000)

#colors
BLACK = (0,0,0)
def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    global time
    global mouseDown
    global background
    global mainBack
    global offset
    global inHandRect
    global fullscreenOn
    global helpOn
    #setup window and initialize game:

    spiderWindow = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('SpiderSolitaire')
    #spiderWindow.fill(backgroundColor)
    mainBack = pygame.transform.smoothscale(mainBack, (windowWidth, windowHeight))
    spiderWindow.blit(mainBack, (0,0))
    initialize(spiderWindow,NoSuits)
    background = spiderWindow.copy()
    pygame.display.flip()
        
    while not game.CheckWin():
        #update the background and inHand image constantly:
        if not inHand.isEmpty() and mouseDown:
            inHandSurf.set_colorkey((0,0,0))
            spiderWindow.blit(background, (0,0))
            inHandX = mouse[0] - offset[0]
            inHandY = mouse[1] - offset[1]
            inHandPos = (inHandX,inHandY)
            spiderWindow.blit(inHandSurf, inHandPos)
            inHandRect.x = inHandX
            inHandRect.y = inHandY
            
            #get info on mouse position
            mouseX = mouse[0] - cardWidth/2
            mouseY = mouse[1] - cardHeight/2
            color = (0,0,0)
            inHandCoord = inHandSurf.get_rect()
            
            #card position,top left corner
            inHandCoord[0] = inHandX-2
            inHandCoord[1] = inHandY-2
            #outline size
            inHandCoord[2] = inHandCoord[2] + 2
            inHandCoord[3] = inHandCoord[3] + 2
            #draw a rectangle outline around the selected cards
            pygame.draw.rect(spiderWindow,color, inHandCoord, 4)
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseDown = True
                updateHitboxes()
                #loc_i is number of stack, loc_j is number of card in that stack (both counted from 0) or (-1,-1) if it is not above any stack.
                loc_i,loc_j = detectCol() 
                
                #check if we're pressing a deal button and have deals left:
                if deal != 0 and detectDeckCol():
                    dealNew(spiderWindow)
                    updateDeck(spiderWindow)
                #skip the loop if mouse isn't pressing anything relevant:
                elif (loc_i,loc_j) == (-1,-1) and inHand.isEmpty():
                    continue
                #if we have cards in our hand, put them down if legal, else return to last position:
                #NOTE: this part is not in use yet. It will implement a different method of moving cards.     
                elif not inHand.isEmpty():
                    n = len(inHand)
                    if (loc_i,loc_j) != (-1,-1) and game.isLegalMove(inHand,stacks[loc_i]):
                        putdownCards(loc_i)
                        updateStack(spiderWindow, loc_i)
                        updateHitbox(loc_i)
                    else:
                        putdownCards(last_i)
                        updateStack(spiderWindow, last_i)
                #if the hand is empty and we're pressing a stack, flip the card if it is face down, if not, pick it up if legal:        
                elif not (loc_i,loc_j) == (-1,-1):
                    if not stacks[loc_i].hasVisible():
                        stacks[loc_i].flip()
                    #If the top card is not hidden, make sure nothing happens if hidden card is pressed.
                    elif loc_j<stacks[loc_i].hidden:
                        continue
                    elif game.isLegalPickup(stacks[loc_i], loc_j): 
                        pickupCards(spiderWindow,(loc_i,loc_j)) #deletes from stack
                        cardLoc = getCardLoc(loc_i,loc_j)
                        offset = (mouse[0]-cardLoc[0],mouse[1]-cardLoc[1])
                    else: 
                        print 'You cant do this'
                    updateStack(spiderWindow, loc_i) 
                    background = spiderWindow.copy()      
            elif event.type == MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                mouseDown = False
                updateHitboxes()
                #loc_i is number of stack, loc_j is number of card in that stack (both counted from 0) or (-1,-1) if it is not above any stack.
                loc_i,loc_j = detectCol()
                #skip the loop if we release with an empty hand:
                if inHand.isEmpty():
                    continue
                #if our hand is not empty, put the cards down where the mouse is released if legal, else return them to their previous position.      
                elif not inHand.isEmpty():
                    n = len(inHand)
                    if (loc_i,loc_j) != (-1,-1):
                        putdownCards(loc_i)
                        #checks if we have a full suit when we put down cards:
                        if checkPile(loc_i):
                            addToPiles(loc_i)
                            spiderWindow.blit(background, (0,0))
                            displayPiles(spiderWindow) 
                            updateStack(spiderWindow, loc_i)
                            updateHitbox(loc_i)
                            game.changeScore(setBonus)
                            displayScore(spiderWindow, font)
                            if(winCond()):
                                print 'you won!'
                        else:
                            updateHitbox(loc_i)
                            spiderWindow.blit(background, (0,0)) 
                            updateStack(spiderWindow, loc_i)
                            if not last_i == loc_i:
                                game.changeScore(movePenalty)
                            displayScore(spiderWindow, font)
                        pygame.display.update()
                    else:
                        putdownCards(last_i)
                        updateHitbox(loc_i)
                        spiderWindow.blit(background, (0,0))
                        updateStack(spiderWindow, last_i)
            elif event.type == KEYDOWN:
                if event.key in (K_f,K_ESCAPE):
                    if fullscreenOn:
                        pygame.display.set_mode((windowWidth,windowHeight))
                        spiderWindow.blit(background,(0,0))
                        pygame.display.flip()
                        
                    else:
                        pygame.display.set_mode((windowWidth,windowHeight), FULLSCREEN)
                        spiderWindow.blit(background,(0,0))
                        pygame.display.flip()
                    fullscreenOn = not fullscreenOn
                #check if input is alt+f4
                if (event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    pygame.quit()
                    sys.exit()
                if event.key == K_h:
                    if helpOn:
                        spiderWindow.blit(background, (0,0))
                        helpOn = False
                    else:                            
                        spiderWindow.blit(helpScreen, (0,0))
                        pygame.display.flip()
                        helpOn = True
            elif event.type == SEC_EVENT:
                time += 1
                displayTime(spiderWindow, font)
                pygame.display.update()
    
    dialog = HSDialog(0)
    dialog.mainLoop()            
                 
    fpsClock.tick(30)


#use: initialize(surface,n)
#pre: surface is a pygame.Surface object, n = 1,2 or 4.
#post: creates a new instance of the Spider Solitaire 'game' with n number of suits in play.
#      surface is the game window.
def initialize(surface, suitNo):
    global game
    global stacks
    global deal
    global m
    global x
    global cardBack
    global aces
    global font
    global helpOn
    global helpScreen
    global hiscores
    
    game = SpiderSolitaire(suitNo)
    stacks = game.getStacks()
    deal = 5
    helpOn = False
    font = pygame.font.Font(None, 30)
    hiscores = LoadScores()
    print hiscores
    
    
    headfont = pygame.font.SysFont(None, 40)
    basicfont = pygame.font.SysFont(None, 30)
    littlefont = pygame.font.SysFont(None, 20)
    text1 = headfont.render('Welcome to Spider Solitaire!', True, (248, 248, 255))
    text2 = basicfont.render('Your objective is to collect 8 full suits. You can put a card down on', True, (248, 248, 255))
    text3 = basicfont.render(' another card if it is one below it in rank. You can only pick up cards', True, (248, 248, 255))
    text4 = basicfont.render(' in rank order of the same suit. Down in the right corner is your deck of', True, (248, 248, 255))
    text5 = basicfont.render('50 cards. You can deal a new row 5 times. Down in the left corner is your', True, (248, 248, 255))
    text6 = basicfont.render('collection of full suits.', True, (248, 248, 255))
    text7 = headfont.render('Good luck and may the odds be ever in your favor!', True, (248, 248, 255))
    text8 = littlefont.render('Press F for fullscreen and H if you would like to see this help again.', True, (248, 248, 255))
    
    helpScreen = pygame.Surface((windowWidth, windowHeight))
    helpScreen.set_alpha(200)
    helpScreen.fill(pygame.Color(0,0,0))
    helpScreen.blit(text1, (windowWidth/2-200,windowHeight/2-200))
    helpScreen.blit(text2, (windowWidth/2-350,windowHeight/2-140))
    helpScreen.blit(text3, (windowWidth/2-350,windowHeight/2-115))
    helpScreen.blit(text4, (windowWidth/2-360,windowHeight/2-90))
    helpScreen.blit(text5, (windowWidth/2-360,windowHeight/2-65))
    helpScreen.blit(text6, (windowWidth/2-350,windowHeight/2-40))
    helpScreen.blit(text7, (windowWidth/2-340,windowHeight/2+20))
    helpScreen.blit(text8, (windowWidth/2-225,windowHeight/2+300))
    
    #calculate space between stacks and coordinates of the stacks.
    m = (windowWidth-10*cardWidth)/11
    for i in range(0,10):
        x.append(i*cardWidth+(i+1)*m)
        
    #we initialize the deck_graphic inside the GUI code instead
    #of initializing it every time a card is displayed, this is done
    #for performance reasons
    global deck_graphic
    
    #this deck graphic uses a colorkey for transparency
    #to remove the black borders that surround each card
    deck_graphic = pygame.image.load('deck_colorkey.png').convert()

    #populate aces with face up images for all suits.
    for i in ['C','D','H','S']:
        cardSurface = SpiderCard(i,1).getImage(deck_graphic)
        cardSurface = pygame.transform.smoothscale(cardSurface, (cardWidth, cardHeight))
        aces.append(cardSurface)
    #get image for the back of card:    
    cardBack = SpiderCard('S',1).getImage(deck_graphic,True)
    cardBack = pygame.transform.smoothscale(cardBack, (cardWidth, cardHeight))
    cardBack.set_colorkey(BLACK)
                          

    updateHitboxes()     
    displayStacks(surface, stacks, x, y)
    displayDeck(surface)
    displayScore(surface, font)

    background = surface.copy()

#use: displayStacks(surface, s, x, y)
#pre: surface is a pygame.Surface object, s an array of SpiderStack objects, x an array of positive integers
#     len(x) = len(s) and y is an integer.
#post:draws stacks in s on surface. Top left corner of s[i] is at (x[i],y)
def displayStacks(surface, Stacks, x, y):
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, Stacks[i], x[i], y)
    pygame.display.update()


#use: displayStack(surface, s, x, y)
#pre: surface is a pygame.Surface object, s is a SpiderStack object, (x,y) are positive coordinates.
#post:draws stack s on surface. Top left corner of s is at (x,y)
def displayStack(surface, Stack, stack_x,stack_y):
        
    cards,hiddenNo = Stack.getStack()
    
    n = len(cards)
    gap = 0
    card_x,card_y = stack_x,stack_y
    for i in range(0,n):
        #determines wheter to use a hidden gap or revealed gap:
        if(i < hiddenNo):
            isHidden=True
            gap = hiddenGap
        else:
            isHidden=False
            gap = revealedGap     
        displayCard(surface,cards[i],isHidden,card_x,card_y,deck_graphic)
        card_y += gap

#use: displayCard(surf, card, hidden, x, y)
#pre: surf is a pygame.Surface object, card is a SpiderCard object, hidden is boolean,  x,y are positive integers
#post: the image of card has been drawn onto surf, face down if hidden, at (x,y)
def displayCard(surface, card, isHidden, card_x, card_y, deck_graphic):
    cardSurf = card.getImage(deck_graphic,isHidden)
    cardSurf = pygame.transform.smoothscale(cardSurf,(cardWidth,cardHeight))
    cardSurf.set_colorkey(BLACK)
    surface.blit(cardSurf, (card_x,card_y))

#use: displayDeck(surf)
#pre: surf is a pygame.Surface object
#post: All remaining deals have been drawn as face down cards on surf
def displayDeck(surface):
    for i in range(0,deal):
        surface.blit(cardBack, (deck_x-i*hiddenGap,deck_y))

# Use:  displayScore(surface, font)
# Pre:  surface is a pygame.Surface object, font is a pygame.font.Font object
# Post: game.score has been updated
def displayScore(surface, font):
    # Todo: change the background color scheme to fit the background
    surface.blit(mainBack, (score_x,score_y),pygame.Rect(score_x, score_y, 150, 30))
    surface.blit(font.render('Score: ' + str(game.score), True, (255,255,255)), (score_x, score_y))

# Use:  displayTime(surf, font)
# Pre:  surf is a Surface, font is a Font
# Post: The game timer has been updated
def displayTime(surface, font):
    surface.blit(mainBack, (timer_x,timer_y),pygame.Rect(timer_x, timer_y, 150, 30))
    surface.blit(font.render(str(time) + 's', True, (255,255,255)), (timer_x, timer_y))

#use: updateStack(surf, num)
#pre: surf is a pygame.Surface object and num is in range(0,len(stacks))
#post: the image of stacks[num] has been updated
def updateStack(surface, i):
    top_x,top_y = getCardLoc(i,0) #loc of top card so we can display Stack in same place
    stack = stacks[i]
    StackBox = stackhboxes[i]
    #surface.fill(backgroundColor, StackBox)
    surface.blit(mainBack, (x[i],y), StackBox)
    displayStack(surface,stack,top_x,top_y)
    pygame.display.update() 

#use: updateStacks(surf)
#pre: surf is a pygame.Surface object
#post: hitboxes and stackhboxes have been updated, Stacks have been re-drawn on surf
def updateStacks(surface):
    for i in range(0,len(stacks)):
        updateHitbox(i)
        updateStack(surface, i)

#use: updateHitboxes()
#post: hitboxes and stackhboxes have been updated for all stacks
def updateHitboxes():
    for i in range(0,colNum):
        updateHitbox(i)

#use: updateHitbox(num)
#pre: num is a valid index for stacks
#post: hitboxes[i] and stackhboxes[i] have been updated.
def updateHitbox(i):
    global hitboxes
    global stackhboxes
    global stackHeight

    stack = stacks[i]
    
    #if the stack is empty, this will create a hitbox to make it possible to add cards to the empty stack
    if stack.isEmpty():
        hitbox = pygame.Rect(x[i],y,cardWidth,cardHeight)
        hitboxes[i] = [hitbox]
        stackhboxes[i] = hitbox
        stackHeight[i] = cardHeight
        return
        
        
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

#Should only be used for debugging purposes!!!
#use: displayStackHitboxes(surf)
#pre: surf is a pygame.Surface object
#post: all elements in stackhboxes have been drawn on surf
def displayStackHitboxes(surface):
    black = pygame.Color(0,0,0)
    for hitbox in stackhboxes:
        pygame.draw.rect(surface, black, hitbox, 2)
    
#use: updateDeckHitbox()
#post: deckBox is up to date
def updateDeckHitbox():
    global deckhboxes
    
    for i in range(0,deal):
        deckBox = pygame.Rect(deck_x-i*hiddenGap,deck_y, cardWidth, cardHeight)
        deckhboxes[i] = deckBox

#use: updateDeck(surf)
#pre: surf is a pygame.Surface object
#post: images of decks have been updated
def updateDeck(surface):
    updateDeckHitbox()
    deckBox = pygame.Rect(deck_x-deal*hiddenGap, deck_y, cardWidth+deal*hiddenGap, cardHeight)
    #surface.fill(backgroundColor, deckBox)
    for rect in deckhboxes:
        pos = (rect.x,rect.y)
        surface.blit(mainBack,pos,rect)
    displayDeck(surface)
    pygame.display.update(deckBox) 

#use: dealNew(surf)
#pre: surf is a pygame.Surface object
#post: one card has been delt on top of each stack
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
        
#use: x,y = getCardLoc(stack_num, card_num)
#pre: stack_num is a valid index of stacks, card_num is a valid index of stacks[stack_num]
#post: (x,y) are the coordinates for the top left corner of stacks[stack_num].cards[card_num]
def getCardLoc(i,j):
    hidden = stacks[i].getStack()[1]
    card_x = x[i]
    card_y = y
    if j <= hidden:
        card_y += j*hiddenGap
    else:
        card_y = (hidden-1)*hiddenGap+((j+1)-hidden)*revealedGap
    return (card_x,card_y)

#use: x,y = detectCol()
#post: stacks[x].cards[y] is the card that was pressed, if no card was pressed (x,y) = (-1,-1)
def detectCol():
    if inHand.isEmpty():
        mouse = pygame.mouse.get_pos()
        for i in range(0,len(stackhboxes)):
            if not stackhboxes[i].collidepoint(mouse):
                continue
            for j in range(0,len(hitboxes[i])):
                h = -(j+1)
                h = len(hitboxes[i])+h
                if hitboxes[i][h].collidepoint(mouse):
                    return (i,h)
    else:
        #print "inHandRect at (%d,%d) w = %d, h = %d"%(inHandRect.x,inHandRect.y,inHandRect.w,inHandRect.h)
        for i in range(0,len(stackhboxes)):
            if stackhboxes[i].colliderect(inHandRect):
                if game.isLegalMove(inHand, stacks[i]):
                    return (i,len(stacks[i])-1)
               
    return (-1,-1)

#use: b = detectDeckCol()
#post: b = True if mouse is over deckhboxes[-1], else False
def detectDeckCol():
    mouse = pygame.mouse.get_pos()
    updateDeckHitbox()
    return deckhboxes[-1].collidepoint(mouse)

#use: pickupCards(surf, (i,j))
#pre: surf is a pygame.Surface object, (i,j) is a tuple, i is a legal index for stacks,
#     and j is a legal index for stacks[i].cards
#post: stacks[i].cards[j:] have been removed form stacks[i]
#      and added to inHand and inHandSurf has been updated
def pickupCards(surface,(i,j)):
    global inHand
    global inHandSurf
    global inHandRect
    global stacks
    global last_i,last_j
    card_x,card_y = getCardLoc(i,j)
    toCopy = pygame.Rect(card_x,card_y,cardWidth,stackHeight[i]-card_y)
    inHandSurf = surface.subsurface(toCopy).copy()
    inHandRect = inHandSurf.get_rect()
    inHand = stacks[i].remove(len(stacks[i])-j)
    last_i = i
    last_j = j

#use: putdownCards(num)
#pre: num is a legal index for stacks
#post: inHand has been added to stacks[i] and is now empty
def putdownCards(i):
    global inHand
    global stacks
    stacks[i].add(inHand)
    clearHand()

#use: clearHand()
#post: inHand is empty and inHandSurf is no picture
def clearHand():
    global inHand
    global inHandSurf
    global inHandRect
    inHand = SpiderStack([],0)
    inHandSurf = pygame.Surface((0,0))
    inHandRect = pygame.Rect(0,0,0,0)

#use: b = checkPile(num)
#pre: num is a legal index for stacks
#post: b = True if the last 13 cards of stacks[i] are in order and of the same suit
def checkPile(i):
    if stacks[i].cards[-1].rank != 1 or len(stacks[i])<13:
        return False
    return game.inSuit(stacks[i], 13)

#use: addToPiles(num)
#pre: num is a legal index for stacks
#post: The last  13 cards of stacks[i] have been removed and
#      a pile of the corresponding suit has been added to piles
def addToPiles(i):
    global piles
    piles.append(stacks[i].remove(13).cards[-1].getSuitNo())

#use: displayPiles(surf)
#pre: surf is a pygame.Surface object
#post: images of the collected piles have been drawn on surf
def displayPiles(surface):
    if len(piles) == 0:
        return
    for i in range(0,len(piles)):
        surface.blit(aces[piles[i]],(pile_x+i*revealedGap,pile_y))

# use:  getDifficulty()
# post: returns the difficulty of the game
def getDifficulty():
    if NoSuits == 1:
        return 'Easy'
    elif NoSuits == 2:
        return 'Medium'
    elif NoSuits == 4:
        return 'Hard'
    
# use:  StoreScore(name, file='highscores.txt')
# pre:  name is the name of the player, file is an optional input for where the file is saved
def StoreScore(name, score, file='highscores.txt'):
    newScore = (name, score, getDifficulty())
    #hiscores.append(newScore)
    output = open(file, 'w')
    for s in hiscores:
        output.write(StoreScoreHelp(s))

def StoreScoreHelp(score):
    outputString = score[0] + ' ' + str(score[1]) + ' ' + score[2]
    return outputString
    
def LoadScores(file='highscores.txt'):
    scorelist = []
    try:
        for line in open(file):
            args = line.split()
            scorelist = scorelist + [(args[0], int(args[1]), args[2])]
    except Exception:
        scorelist = []
    return scorelist
    


#use: b = winCond()
#post: b = True if the game is won, b = False otherwise.    
def winCond():
    return len(piles) == 8

if __name__ == '__main__':
    main()
     
pygame.quit()
