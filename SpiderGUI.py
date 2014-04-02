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
sizeOfWindowsBar = 38
systemHeight = GetSystemMetrics(1)-sizeOfWindowsBar
windowWidth = min(systemWidth, 1500)
windowHeight = min(systemHeight, 850)-sizeOfWindowsBar
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
revealedGapByStack = []
#Coordinates of the deck.
deck_x = windowWidth - 200
deck_y = windowHeight - 150
#Coordinates of the full suits (='a pile') the user has collected.
pile_x = 30
pile_y = windowHeight - 150
#Coordinates of the timer
timer_x = windowWidth/2 + 40
timer_y = 4
#Coordinates of the score
score_x = windowWidth/2 - 60
score_y = 4
#coordinates of instructions
instr_x = windowWidth-297
instr_y = 4
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
spiderBox = 0 #for the settings button
menuButtons = [] #for the menu buttons
#variables for the stacks:
stackHeight = [0]*colNum
stacks = []
#this instance of spider solitaire:
game = SpiderSolitaire(1)
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
mainBack = pygame.image.load('Backgrounds/vintage.jpg')
#for help on/off:
helpOn = False
#for highscore screen on/off:
hsOn = False
#for all option screens we create a dark overlay:
overlay = 0
#for settings:
menuOn = False

fullscreenOn = False

# Initializes the game timer
time = 0
SEC_EVENT = USEREVENT + 1
pygame.time.set_timer(SEC_EVENT, 1000)

hiscores = []

#colors
BLACK = (0,0,0)
def play(spiderWindow):
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

    #spiderWindow = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('SpiderSolitaire')
    #spiderWindow.fill(backgroundColor)
    mainBack = pygame.transform.smoothscale(mainBack, (windowWidth, windowHeight))
    spiderWindow.blit(mainBack, (0,0))
    initialize(spiderWindow,NoSuits)
    background = spiderWindow.copy()
    pygame.display.flip()
        
    while not winCond():
        #update the background and inHand image constantly:
        if not inHand.isEmpty() and mouseDown:
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
            inHandCoord[2] = inHandCoord[2] + 3
            inHandCoord[3] = inHandCoord[3] + 3
            #draw a rectangular outline around the selected cards
            pygame.draw.rect(spiderWindow,color, inHandCoord, 4)
            displayTime(spiderWindow, font)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not helpOn and not hsOn and not mouseDown:
                mouseDown = True
                updateHitboxes()
                #loc_i is number of stack, loc_j is number of card in that stack (both counted from 0) or (-1,-1) if it is not above any stack.
                loc_i,loc_j = detectCol() 
                
                if detectSettingsCol():
                    toggleMenu(spiderWindow)
                elif menuOn:
                    continue
                #check if we're pressing a deal button and have deals left:
                elif deal != 0 and detectDeckCol():
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
            elif event.type == MOUSEMOTION and not helpOn and not hsOn:
                mouse = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP and not helpOn and not hsOn:
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
                                createWin(spiderWindow)
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
                elif (event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    pygame.quit()
                    sys.exit()
                elif event.key == K_h:
                    toggleHelp(spiderWindow)
            if event.type == SEC_EVENT and not (helpOn or menuOn):
                time += 1
                displayTime(spiderWindow, font)
                pygame.display.update()
                    
    if isHighScore(game.score) or True:
        gettext.install("highscore")
        dialog = HSDialog(0)
        dialog.MainLoop()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                break       
                 
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
    global overlay
    global hiscores
    global time
    global revealedGapByStack
    
    overlay = pygame.Surface((windowWidth, windowHeight))
    overlay.set_alpha(200)
    overlay.fill(pygame.Color(0,0,0))
    
    surface.blit(mainBack,(0,0))
    game = SpiderSolitaire(suitNo)
    stacks = game.getStacks()
    revealedGapByStack = [revealedGap]*len(stacks)
    deal = 5
    helpOn = False
    font = pygame.font.Font(None, 18)
    hiscores = LoadScores()
    createMenuButton(surface)
    
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
    displayDeck(surface)
    displayScore(surface, font)     
    displayStacks(surface, stacks, x, y)
    
    #normal_font = pygame.font.SysFont(None, 18)
    #gray = (200,200,200)
    #instructions = normal_font.render("Press h for help and f for fullscreen mode", True,gray)
    
    #surface.blit(instructions,(instr_x,instr_y))
    time = 0
    background = surface.copy()
    
#use: changeBackground(path, surface)
#pre: path is a legal path to an image file and surface is a pygame surface
#post: The game now displays the image at path as it's background
def changeBackground(path, surface):
    global mainBack
    mainBack = pygame.image.load(path).convert()
    mainBack = pygame.transform.smoothscale(mainBack,(windowWidth, windowHeight))
    surface.blit(mainBack,(0,0))
    displayDeck(surface)
    displayPiles(surface)
    displayScore(surface,font)
    createMenuButton(surface)
    displayStacks(surface, stacks, x, y)
    


#use: createHelp()
#post: creates the win screen for the game
def createWin(surface):
    global overlay
    winfont = pygame.font.SysFont(None, 70)
    text9 = winfont.render('You won!', True, (248, 248, 255))
    surface.blit(overlay, (0,0))
    surface.blit(text9, (windowWidth/2-100, windowHeight/2-150))

#use: createMenuButton(window)
#pre: window is a pygame surface
#post: creates a menu button in the down right corner that looks like a spider.
def createMenuButton(surface):
    global spiderBox
    spiderW = 60
    spiderH = 60
    spider = pygame.image.load('spider.png').convert_alpha()
    spider = pygame.transform.smoothscale(spider, (spiderW, spiderH))
    surface.blit(spider, (windowWidth-65, windowHeight-65))
    spiderBox = pygame.Rect(windowWidth-65, windowHeight-65, spiderW, spiderH)
    pygame.display.update(spiderBox)
   
def toggleMenu(surface):
    global menuOn
    global background
    if not menuOn:
        background = surface.copy()
        menuOn = True
        menu(surface)
    else:
        menuOn = False
        surface.blit(background, (0,0))
        pygame.display.flip()

#use: menu(surface)
#pre: surface is a pygame surface
#post: creates a menu screen with it's own loop over the game with various options.
def menu(surface):
    global overlay
    global menuButtons
    global menuOn
    global background
    
    
    bWidth = 300
    bHeight = 100
    x_loc = windowWidth/2-120
    y_loc = windowHeight/2-200
    y_locs = [y_loc, y_loc+bHeight, y_loc+2*bHeight, y_loc+3*bHeight]
    
    gameSurf = pygame.Surface((bWidth, bHeight))
    diffSurf =  pygame.Surface((bWidth,bHeight))
    scoreSurf =  pygame.Surface((bWidth, bHeight))
    helpSurf = pygame.Surface((bWidth,bHeight))
    
    font = pygame.font.Font('fonts/FancyCardText.ttf', 72)
    game = font.render('New Game', True, (248, 248, 255))
    gameSurf.blit(game, (0,0))
    diff = font.render('Settings', True, (248, 248, 255))
    diffSurf.blit(diff, (0,0))
    score = font.render('High Scores', True, (248, 248, 255))
    scoreSurf.blit(score, (0,0))
    help = font.render('Help', True, (248, 248, 255))
    helpSurf.blit(help, (0,0))
    
    menuSurfaces = [gameSurf, diffSurf, scoreSurf, helpSurf]
    
    gameButton = gameSurf.get_rect()
    gameButton.x,gameButton.y = (x_loc,y_locs[0])
    diffButton = diffSurf.get_rect()
    diffButton.x,diffButton.y = (x_loc,y_locs[1])
    scoreButton = scoreSurf.get_rect()
    scoreButton.x,scoreButton.y = (x_loc,y_locs[2])
    helpButton = helpSurf.get_rect()
    helpButton.x,helpButton.y = (x_loc,y_locs[3])
    menuButtons = [gameButton, diffButton, scoreButton, helpButton]
                
    surface.blit(overlay, (0,0))
    for i in range(0,len(menuSurfaces)):
        menuSurfaces[i].set_colorkey(pygame.Color(0,0,0))
        surface.blit(menuSurfaces[i], (x_loc, y_locs[i]))
        createMenuButton(surface)
    
    pygame.display.flip()
    
    
    while menuOn:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                i = detectMenuCol()
                if detectSettingsCol():
                    toggleMenu(surface)
                    menuOn = False
                # New game
                elif i==0:
                    toggleMenu(surface)
                    menuOn = False
                    initialize(surface,NoSuits)
                # Settings
                elif i==1:
                    settingsMenu(surface)
                # Highscores
                elif i==2:
                    menuOn = False
                    surface.blit(background, (0,0))
                    toggleHighscores(surface)
                # Help
                elif i==3:
                    menuOn = False
                    surface.blit(background, (0,0))
                    toggleHelp(surface)

def toggleSettings(surface):
    global background
    global hsOn
    global hsScreen
    
    if hsOn:
        surface.blit(background, (0,0))
        pygame.display.flip()
        hsOn = False
    else: 
        background = surface.copy()                           
        highscoresMenu(surface)
                    
#use: selectBackgroundMenu():
#post: The user has been given a graphical menu to choose a background and mainBack is his background of choice
def settingsMenu(surface):
    global mainBack
    global BackgroundMenuOn
    global background
    surface.blit(background,(0,0))
    surface.blit(overlay,(0,0))
    
    back_x = 50
    back_y = windowHeight - 100
    back_width = 100
    back_height = 50
    font = pygame.font.Font('fonts/FancyCardText.ttf', 75)
    backfont = pygame.font.Font('fonts/FancyCardText.ttf', 50)
    
    backSurf = pygame.Surface((back_width, back_height))
    backSurf.set_colorkey(pygame.Color(0,0,0))
    back = backfont.render('Back', True, (248, 248, 255))
    backSurf.blit(back, (0,0))
    
    #We want 4 thumbnails per line
    thumbWidth = windowWidth/5
    thumbHeight = int(thumbWidth*(float(windowHeight)/windowWidth))
    spaceBetween = (windowWidth-4*thumbWidth)/5
    backgroundFolder = 'Backgrounds/'
    thumbfile = ['grumpy_thumb.jpg','nes_thumb.jpg','panda_thumb.jpg','pandaprogrammer_thumb.jpg','pandasuit_thumb.jpg','pulp_star_thumb.jpg','vintage_thumb.jpg']
    backgroundFile = ['grumpy.jpg','nes.jpg','panda.jpg','pandaprogrammer.jpg','pandasuit.jpg','pulp_star.jpg','vintage.jpg']
    thumbnails = []
    for image in thumbfile:
        tempSurf = pygame.image.load(backgroundFolder+image).convert()
        tempSurf = pygame.transform.smoothscale(tempSurf,(thumbWidth,thumbHeight))
        thumbnails.append(tempSurf)
    thumbX = spaceBetween
    thumbY = thumbHeight
    selection = []
    for thumbnail in thumbnails:
        if thumbX+thumbWidth>windowWidth:
            thumbX = spaceBetween
            thumbY = 2*thumbHeight+spaceBetween
        surface.blit(thumbnail,(thumbX,thumbY))
        tempRect = pygame.Rect(thumbX,thumbY,thumbWidth,thumbHeight)
        selection.append(tempRect)
        thumbX += thumbWidth+spaceBetween
    surface.blit(backSurf, (back_x, back_y))
    createMenuButton(surface)
    pygame.display.flip()
    BackgroundMenuOn = True
    while BackgroundMenuOn:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                overBackgroundNr = -1
                for i in range(0,len(selection)):
                    if selection[i].collidepoint(mousePos):
                        overBackgroundNr = i
                print overBackgroundNr
                if overBackgroundNr >= 0:
                    print 'changing background to '+backgroundFolder+backgroundFile[overBackgroundNr]
                    changeBackground(backgroundFolder+backgroundFile[overBackgroundNr],surface)
                    background = surface.copy()
                    toggleMenu(surface)
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    mouseXY = pygame.mouse.get_pos()
                    back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
                    if back_rect.collidepoint(mouseXY):
                        toggleHighscores(surface)
                elif detectMenuCol():
                    toggleMenu(surface)
                    return

pygame.quit()

                    
def toggleHighscores(surface):
    global background
    global hsOn
    global hsScreen
    
    if hsOn:
        surface.blit(background, (0,0))
        pygame.display.flip()
        hsOn = False
    else: 
        background = surface.copy()                           
        highscoresMenu(surface)

def highscoresMenu(surface):
    global hsScreen
    global backButton
    global hsOn
    
    hsOn = True
    
    hsScreen = pygame.Surface((windowWidth, windowHeight))
    hsScreen.set_alpha(200)
    hsScreen.fill(pygame.Color(0,0,0))
    surface.blit(hsScreen, (0,0))
    
    back_x = 50
    back_y = windowHeight - 100
    back_width = 100
    back_height = 50
    font = pygame.font.Font('fonts/FancyCardText.ttf', 75)
    backfont = pygame.font.Font('fonts/FancyCardText.ttf', 50)
    
    backSurf = pygame.Surface((back_width, back_height))
    backSurf.set_colorkey(pygame.Color(0,0,0))
    back = backfont.render('Back', True, (248, 248, 255))
    backSurf.blit(back, (0,0))
    
    if windowWidth > 1024:
        labels_y = 100
        name_label_x = 300
        score_label_x = 600
        diff_label_x = 900
        scores_y = labels_y + 100
    else:
        labels_y = 20
        name_label_x = 100
        score_label_x = 400
        diff_label_x = 700
        medal_pos = (windowWidth-200,windowHeight-285)
        scores_y = labels_y + 100
        
    name_label = font.render('Name', True, (248, 248, 255))
    score_label = font.render('Score', True, (248, 248, 255))
    diff_label = font.render('Difficulty', True, (248, 248, 255))
    
    
    
    scorefont = pygame.font.SysFont(None, 24)
    top_scores = LoadScores()
    
    max_scores = 15 #specify max number of high scores to be displayed
    score_cnt = 0
    
    for score in top_scores:
        if score_cnt > max_scores:
            break
        name_val = score[0]
        score_val = str(score[1])
        level_val = score[2]
        name = scorefont.render(name_val, True, (248, 248, 255))
        score = scorefont.render(score_val, True, (248, 248, 255))
        diff = scorefont.render(level_val, True, (248, 248, 255))
        surface.blit(name, (name_label_x, scores_y))
        surface.blit(score, (score_label_x, scores_y))
        surface.blit(diff, (diff_label_x, scores_y))                
        score_cnt += 1
        scores_y += 30

    surface.blit(backSurf, (back_x, back_y))
    surface.blit(name_label, (name_label_x, labels_y))
    surface.blit(score_label, (score_label_x, labels_y))
    surface.blit(diff_label, (diff_label_x, labels_y))
    
    pygame.display.update()
    
    while hsOn:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseXY = pygame.mouse.get_pos()
                back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
                if back_rect.collidepoint(mouseXY):
                    toggleHighscores(surface)
                    toggleMenu(surface)
            elif event.type == KEYDOWN:
                if event.key in (K_s, K_ESCAPE):
                    toggleHighscores(surface)
                    toggleMenu(surface)   


def toggleHelp(surface):
    global background
    global helpOn
    if helpOn:
        surface.blit(background, (0,0))
        pygame.display.flip()
        helpOn = False
    else: 
        background = surface.copy()                           
        helpMenu(surface)


#use: helpMenu()
#pre: surface is a pygame surface
#post: creates the Help screen for the game
def helpMenu(surface):
    global overlay
    global helpOn
    
    helpOn = True
    
    back_x = 50
    back_y = windowHeight - 100
    back_width = 100
    back_height = 50
    font = pygame.font.Font('fonts/FancyCardText.ttf', 75)
    backfont = pygame.font.Font('fonts/FancyCardText.ttf', 50)
    
    backSurf = pygame.Surface((back_width, back_height))
    backSurf.set_colorkey(pygame.Color(0,0,0))
    back = backfont.render('Back', True, (248, 248, 255))
    backSurf.blit(back, (0,0))
    
    headfont = pygame.font.SysFont(None, 70)
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

    surface.blit(overlay, (0,0))
    surface.blit(text1, (windowWidth/2-350,windowHeight/2-200))
    surface.blit(text2, (windowWidth/2-350,windowHeight/2-120))
    surface.blit(text3, (windowWidth/2-350,windowHeight/2-95))
    surface.blit(text4, (windowWidth/2-360,windowHeight/2-70))
    surface.blit(text5, (windowWidth/2-360,windowHeight/2-45))
    surface.blit(text6, (windowWidth/2-350,windowHeight/2-20))
    surface.blit(text7, (windowWidth/2-600,windowHeight/2+150))
    surface.blit(text8, (windowWidth/2-225,windowHeight/2+300))
    
    surface.blit(backSurf, (back_x, back_y))
    
    pygame.display.flip()
    
    while helpOn:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseXY = pygame.mouse.get_pos()
                back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
                if back_rect.collidepoint(mouseXY):
                    toggleHelp(surface)
                    toggleMenu(surface)
            elif event.type == KEYDOWN:
                if event.key in (K_h,K_ESCAPE):
                    toggleHelp(surface)
                    toggleMenu(surface)
                    

#use: displayStacks(surface, s, x, y)
#pre: surface is a pygame.Surface object, s an array of SpiderStack objects, x an array of positive integers
#     len(x) = len(s) and y is an integer.
#post:draws stacks in s on surface. Top left corner of s[i] is at (x[i],y)
def displayStacks(surface, Stacks, x, y):
    n = len(Stacks)
    for i in range(0,n):
        displayStack(surface, i, x[i], y)
    pygame.display.update()


#use: displayStack(surface, i, x, y)
#pre: surface is a pygame.Surface object, i is a legal index to stacks, (x,y) are positive coordinates.
#post:draws stack s on surface. Top left corner of s is at (x,y)
def displayStack(surface, i, stack_x,stack_y):
        
    cards,hiddenNo = stacks[i].getStack()
    
    n = len(cards)
    gap = 0
    card_x,card_y = stack_x,stack_y
    for j in range(0,n):
        #determines wheter to use a hidden gap or revealed gap:
        if(j < hiddenNo):
            isHidden=True
            gap = hiddenGap
        else:
            isHidden=False
            gap = revealedGapByStack[i]     
        displayCard(surface,cards[j],isHidden,card_x,card_y,deck_graphic)
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
    surface.blit(mainBack, (score_x,score_y),pygame.Rect(score_x, score_y, 150, 15))
    surface.blit(font.render('Score: ' + str(game.score), True, (255,255,255)), (score_x, score_y))

# Use:  displayTime(surf, font)
# Pre:  surf is a Surface, font is a Font
# Post: The game timer has been updated
def displayTime(surface, font):
    if not helpOn:
        surface.blit(mainBack, (timer_x,timer_y),pygame.Rect(timer_x, timer_y, 100, 15))
        surface.blit(font.render('Time: '+str(time) + 's', True, (255,255,255)), (timer_x, timer_y))

        
#use: updateStack(surf, num)
#pre: surf is a pygame.Surface object and num is in range(0,len(stacks))
#post: the image of stacks[num] has been updated
def updateStack(surface, i):
    top_x,top_y = getCardLoc(i,0) #loc of top card so we can display Stack in same place
    maxHeight = deck_y-y-20
    stack = stacks[i]
    noHidden = stack.hidden
    noVisible = len(stack)-noHidden
    stackHeight = noHidden*hiddenGap+(noVisible-1)*revealedGap+cardHeight
    if stackHeight > maxHeight:
        revealedGapByStack[i] = (maxHeight-cardHeight-noHidden*hiddenGap)/(noVisible-1)
    else:
        revealedGapByStack[i] = revealedGap
    
    StackBox = stackhboxes[i]
    #surface.fill(backgroundColor, StackBox)
    surface.blit(mainBack, (x[i],y), StackBox)
    displayStack(surface,i,top_x,top_y)
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
    stackHeight[i] = hitstack[-1].y-hitstack[0].y+cardHeight
    stackhbox = pygame.Rect(x[i],y,cardWidth,stackHeight[i]+10)
    stackhboxes[i] = stackhbox

#Should only be used for debugging purposes!!!
#use: displayStackHitboxes(surf)
#pre: surf is a pygame.Surface object
#post: all elements in stackhboxes have been drawn on surf
def displayStackHitboxes(surface):
    black = pygame.Color(0,0,0)
    for hitbox in stackhboxes:
        pygame.draw.rect(surface, black, hitbox, 4)
    
#use: updateDeckHitbox()
#post: deckBox is up to date
def updateDeckHitbox():
    global deckhboxes
    deckhboxes = []
    for i in range(0,deal):
        deckBox = pygame.Rect(deck_x-i*hiddenGap,deck_y, cardWidth, cardHeight)
        deckhboxes.append(deckBox)

#use: updateDeck(surf)
#pre: surf is a pygame.Surface object
#post: images of decks have been updated
def updateDeck(surface):
    deckBox = pygame.Rect(deck_x-deal*hiddenGap, deck_y, cardWidth+deal*hiddenGap, cardHeight)
    #surface.fill(backgroundColor, deckBox)
    for rect in deckhboxes:
        pos = (rect.x,rect.y)
        surface.blit(mainBack,pos,rect)
    displayDeck(surface)
    pygame.display.update(deckBox) 
    updateDeckHitbox()

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
        card_y = (hidden-1)*hiddenGap+((j+1)-hidden)*revealedGapByStack[i]
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
                    #print (i,h)
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

#use: b = detectSettingsCol()
#post: b = True if mouse is over settings symbol, else false
def detectSettingsCol():
    mouse = pygame.mouse.get_pos()
    return spiderBox.collidepoint(mouse)
    
def detectMenuCol():
    mouse = pygame.mouse.get_pos()
    for i in range(0,len(menuButtons)):
        if menuButtons[i].collidepoint(mouse):
            return i
    
    return -1
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
    #toCopy = pygame.Rect(card_x,card_y,cardWidth,stackHeight[i]-card_y+y)
    offsetGap = 30-revealedGapByStack[i]
    toCopy = pygame.Rect(card_x,card_y+offsetGap,cardWidth,stackHeight[i]-card_y+y)

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
def StoreScore(name, score, filename='highscores.txt'):
    newScore = (name, score, getDifficulty())
    if len(hiscores) >= 10:
        hiscores[10] = newScore
    else:
        hiscores.append(newScore)
    hiscores.sort()
    resetFile(filename)
    for s in range(0, len(hiscores)):
        AddScoreToFile(hiscores[s])

# Use:  resetFile(file)
# Pre:  file is a filename
# Post: file is empty
def resetFile(filename):
    open(filename, 'w')

# Use:  AddScoreToFile(score, filename)
# Pre:  score is a score tuple. filename is the name of the file to store it in
# Post: score has been added at the bottom of the file filename
def AddScoreToFile(score, filename='highscores.txt'):
    output = open(filename, 'a')
    output.write(StoreScoreHelp(score))

# Use:  s = StoreScoreHelp(score)
# Pre:  score is a score tuple
# Post: s is a string containing the formatted version of score
def StoreScoreHelp(score):
    outputString = score[0] + ' ' + str(score[1]) + ' ' + score[2] + '\n'
    return outputString
    
# Use:  scores = LoadScores()
#       Optional input: filename
# Pre:  filename is the name of the file to retrieve the scores from
# Post: scores contains the scores in file filename
def LoadScores(filename='highscores.txt'):
    scorelist = []
    try:
        for line in open(filename):
            args = line.split()
            scorelist = scorelist + [(args[0], int(args[1]), args[2])]
    except Exception:
        scorelist = []
    return sorted(scorelist, key=lambda x: -x[1])

# use:  isHighScore(n)
# pre:  n is a positive integer
# post: if n is higher than the lowest high score, returns True. False otherwise
def isHighScore(n):
    if len(hiscores)==0:
        return True
    return n > hiscores[-1:][0]


#use: b = winCond()
#post: b = True if the game is won, b = False otherwise.    
def winCond():
    return len(piles) == 8

#use: selectBackgroundMenu():
#post: The user has been given a graphical menu to choose a background and mainBack is his background of choice
def settingsMenu(surface):
    global mainBack
    global BackgroundMenuOn
    global background
    surface.blit(background,(0,0))
    surface.blit(overlay,(0,0))
    #We want 4 thumbnails per line
    thumbWidth = windowWidth/5
    thumbHeight = int(thumbWidth*(float(windowHeight)/windowWidth))
    spaceBetween = (windowWidth-4*thumbWidth)/5
    backgroundFolder = 'Backgrounds/'
    thumbfile = ['grumpy_thumb.jpg','nes_thumb.jpg','panda_thumb.jpg','pandaprogrammer_thumb.jpg','pandasuit_thumb.jpg','pulp_star_thumb.jpg','vintage_thumb.jpg']
    backgroundFile = ['grumpy.jpg','nes.jpg','panda.jpg','pandaprogrammer.jpg','pandasuit.jpg','pulp_star.jpg','vintage.jpg']
    thumbnails = []
    for image in thumbfile:
        tempSurf = pygame.image.load(backgroundFolder+image).convert()
        tempSurf = pygame.transform.smoothscale(tempSurf,(thumbWidth,thumbHeight))
        thumbnails.append(tempSurf)
    thumbX = spaceBetween
    thumbY = thumbHeight
    selection = []
    for thumbnail in thumbnails:
        if thumbX+thumbWidth>windowWidth:
            thumbX = spaceBetween
            thumbY = 2*thumbHeight+spaceBetween
        surface.blit(thumbnail,(thumbX,thumbY))
        tempRect = pygame.Rect(thumbX,thumbY,thumbWidth,thumbHeight)
        selection.append(tempRect)
        thumbX += thumbWidth+spaceBetween
    createMenuButton(surface)
    pygame.display.flip()
    BackgroundMenuOn = True
    while BackgroundMenuOn:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                overBackgroundNr = -1
                for i in range(0,len(selection)):
                    if selection[i].collidepoint(mousePos):
                        overBackgroundNr = i
                print overBackgroundNr
                if overBackgroundNr >= 0:
                    print 'changing background to '+backgroundFolder+backgroundFile[overBackgroundNr]
                    changeBackground(backgroundFolder+backgroundFile[overBackgroundNr],surface)
                    background = surface.copy()
                    toggleMenu(surface)
                    return
                elif detectMenuCol():
                    toggleMenu(surface)
                    return

pygame.quit()
