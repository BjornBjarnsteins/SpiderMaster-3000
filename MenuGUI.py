import pygame, sys, os, random, time, math
import SpiderGUI
from pygame.locals import * 

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
    
    width = 1024
    height = 600
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SpiderMaster-3000')

    #colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    LIGHTGREEN = (185,255,185)
    RED = (255,0,0)
    FPS = 70 #FPS controls the framerate of our display
        
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
    fontEasy = TextItem("{easy}",position=(width/2,1.85*height/6),font="fonts/{PixelFlag}.ttf",color=BLACK,
                            fontSize=fontSizeMenu)
    fontMedium = TextItem("{medium}",position=(width/2,2.45*height/6),font="fonts/{PixelFlag}.ttf",
                              color=BLACK,fontSize=fontSizeMenu)
    fontHard = TextItem("{hard}",position=(width/2,3.05*height/6),font="fonts/{PixelFlag}.ttf",
                       color=BLACK,fontSize=fontSizeMenu)       
    #position of suits
    suitClub = (0,0)
    suitHeart = (0,160)
    suitDiamond = (160,0)
    suitSpade = (160,160)
    suitSize = (suitWidth,suitHeight)
    
    #pre: posX is float, turnSize and suitPos are integers
    #post: draws the mouseOver animation
    def animation(posX,turnSize,suitPos):
        suitSurf.blit(suits,(0,0),(suitPos,suitSize))
        surf = pygame.transform.scale(suitSurf,(turnSize,suitWidth))
        offsetX = suitWidth-turnSize/2
        spadePos = (posX*width+offsetX,0.63*height)
        screen.blit(surf,spadePos)
        
    while True:
        #draw background
        screen.fill(LIGHTGREEN)
    
        title = TextItem("Spider Solitaire",position=(width/2,0.85*height/6),
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
                    easy.main()
                if fontMedium.position.collidepoint(eventX,eventY):
                    medium = SpiderGUI
                    medium.NoSuits = 2
                    medium.main()
                if fontHard.position.collidepoint(eventX,eventY):
                    hard = SpiderGUI
                    hard.NoSuits = 4
                    hard.main()     
        #if mouse hovers on window              
        if pygame.mouse.get_focused():
            eventX,eventY= pygame.mouse.get_pos()
            seconds = time.clock()*3
            turnSize = math.fabs(math.sin(seconds))
            turnSize = int(turnSize*suitWidth)+1
            #draw mouse focus animation and color text depending on which button the cursor 
            #is hovering over
            if fontEasy.position.collidepoint(eventX,eventY):
                fontEasy.textSurface = fontEasy.render('{easy}',False,RED)
                animation(0.34,turnSize,suitSpade)
            elif fontMedium.position.collidepoint(eventX,eventY):
                fontMedium.textSurface = fontMedium.render('{medium}',False,RED)            
                animation(0.42,turnSize,suitSpade)
                animation(0.25,turnSize,suitHeart)
            elif fontHard.position.collidepoint(eventX,eventY):
                fontHard.textSurface = fontHard.render('{hard}',False,RED)                
                animation(0.42,turnSize,suitSpade)
                animation(0.25,turnSize,suitHeart)
                animation(0.59,turnSize,suitDiamond)
                animation(0.08,turnSize,suitClub)  
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
