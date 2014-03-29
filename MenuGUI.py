import pygame, sys, os, random, time, math
import SpiderGUI
from pygame.locals import * 
from win32api import GetSystemMetrics

class TextItem (pygame.font.Font):
    
    #pre: text is a string, position is a tuple, font is the font's location, 
    #     color is a Color object,fontSize is a positive integer
    def __init__(self, text, position, font,color,fontSize, antialias=1, background=None):
        pygame.font.Font.__init__(self, font, fontSize)
        self.text = text
        if background == None:
            self.textSurface = self.render(self.text, antialias, color)
        else:
            self.textSurface = self.render(self.text, antialias, color, background)

        self.position = self.textSurface.get_rect(centerx=position[0], centery=position[1])

def main():
    #Set window position at top left corner
    windowX = 0
    windowY = 30
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX,windowY)
    
    sizeOfWindowsBar = 38

    #screen dimensions:
    systemWidth = GetSystemMetrics(0)
    systemHeight = GetSystemMetrics(1)-sizeOfWindowsBar
    windowWidth = min(systemWidth, 1500)
    windowHeight = min(systemHeight, 850)-sizeOfWindowsBar
    
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('SpiderMaster-3000')

    #colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    LIGHTGREEN = (185,255,185)
    RED = (255,0,0)
    FPS = 60 #FPS controls the framerate of our display
        
    #graphics
    suits = pygame.image.load('images/suits.png').convert()
    
    suitWidth = 160
    suitHeight = 160
    suitSurf = pygame.Surface((suitWidth,suitHeight))


    clock = pygame.time.Clock()
        
    #Set size of title
    fontSizeTitle = 800

    #Menu dialog
    fontSizeMenu = 42
    fontEasy = TextItem("{easy}",position=(windowWidth/2,1.85*windowHeight/6),font="fonts/{PixelFlag}.ttf",color=BLACK,
                            fontSize=fontSizeMenu)
    fontMedium = TextItem("{medium}",position=(windowWidth/2,2.45*windowHeight/6),font="fonts/{PixelFlag}.ttf",
                              color=BLACK,fontSize=fontSizeMenu)
    fontHard = TextItem("{hard}",position=(windowWidth/2,3.05*windowHeight/6),font="fonts/{PixelFlag}.ttf",
                       color=BLACK,fontSize=fontSizeMenu)       
    #position of suits
    suitClub = (0,0)
    suitHeart = (0,160)
    suitDiamond = (160,0)
    suitSpade = (160,160)
    suitSize = (suitWidth,suitHeight)
    
    #pre: distanceFromMid is float, turnSize and suitPos are integers
    #post: draws the mouseOver animation
    def animation(distanceFromMid,turnSize,suitPos):
        suitSurf.blit(suits,(0,0),(suitPos,suitSize))
        surf = pygame.transform.scale(suitSurf,(turnSize,suitWidth))
        offsetX = suitWidth-turnSize/2
        spadePos = (distanceFromMid+(windowWidth/2)+offsetX-suitWidth,0.63*windowHeight)
        screen.blit(surf,spadePos)
        
    while True:
        #draw background
        screen.fill(LIGHTGREEN)
    
        title = TextItem("Spider Solitaire",position=(windowWidth/2,0.85*windowHeight/6),
                                    font="fonts/PixelMusketeer.ttf",color=BLACK,fontSize=fontSizeTitle)
        screen.blit(title.textSurface,title.position)
        #event cases
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #user chooses difficulty level/number of suits
            if event.type == MOUSEBUTTONDOWN:
                if fontEasy.position.collidepoint(eventX,eventY):
                    easy = SpiderGUI
                    easy.NoSuits = 1
                    easy.play(screen)
                if fontMedium.position.collidepoint(eventX,eventY):
                    medium = SpiderGUI
                    medium.NoSuits = 2
                    medium.play(screen)
                if fontHard.position.collidepoint(eventX,eventY):
                    hard = SpiderGUI
                    hard.NoSuits = 4
                    hard.play(screen)
        #if mouse is inside our window              
        if pygame.mouse.get_focused():
            eventX,eventY= pygame.mouse.get_pos()
            seconds = time.clock()*3
            #turnSize is the width size of any of the suit graphics
            turnSize = math.fabs(math.sin(seconds))
            turnSize = int(turnSize*suitWidth)+1

            #specify distances from the midpoint for each suits
            distanceSpade = 200*0.5
            distanceHeart = -200*0.5
            distanceDiamond = 200*1.5
            distanceClub = -200*1.5
            #draw mouse focus animation and color text depending on which button the cursor 
            #is hovering over
            if fontEasy.position.collidepoint(eventX,eventY):
                distance = 0
                fontEasy.textSurface = fontEasy.render('{easy}',False,RED)
                fontMedium.textSurface = fontEasy.render('{medium}',False,BLACK)
                fontHard.textSurface = fontEasy.render('{hard}',False,BLACK)
                animation(distance,turnSize,suitSpade)
            elif fontMedium.position.collidepoint(eventX,eventY):
                fontMedium.textSurface = fontMedium.render('{medium}',False,RED)
                fontEasy.textSurface = fontEasy.render('{easy}',False,BLACK)
                fontHard.textSurface = fontEasy.render('{hard}',False,BLACK)
                animation(distanceSpade,turnSize,suitSpade)
                animation(distanceHeart,turnSize,suitHeart)
            elif fontHard.position.collidepoint(eventX,eventY):
                fontHard.textSurface = fontHard.render('{hard}',False,RED)
                fontMedium.textSurface = fontEasy.render('{medium}',False,BLACK)
                animation(distanceSpade,turnSize,suitSpade)
                animation(distanceHeart,turnSize,suitHeart)
                animation(distanceDiamond,turnSize,suitDiamond)
                animation(distanceClub,turnSize,suitClub)  
            #otherwise we set the text to its default color
            else:
                fontEasy.textSurface = fontEasy.render('{easy}',False,BLACK)
                fontMedium.textSurface = fontEasy.render('{medium}',False,BLACK)
                fontHard.textSurface = fontEasy.render('{hard}',False,BLACK)

                 
        if fontSizeTitle > 100:
            #animate title sequence
            fontSizeTitle = int(fontSizeTitle*0.8)            
        screen.blit(fontEasy.textSurface,fontEasy.position)
        screen.blit(fontMedium.textSurface,fontMedium.position)
        screen.blit(fontHard.textSurface,fontHard.position)
        clock.tick(FPS)
        pygame.display.flip()

if __name__ == '__main__':
    main()
