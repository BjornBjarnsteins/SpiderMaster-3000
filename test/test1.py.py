import pygame
import sys
from pygame.locals import *
#TEST

#some basic colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)

#define window display size
screen_size_x = 600
screen_size_y = 500
screen = pygame.display.set_mode((screen_size_x,screen_size_y),pygame.HWSURFACE)
#title of this test
pygame.display.set_caption('solitaire graphic test')


FPS = 30 #FPS is a global variable that controls the framerate of our display

#load the graphic that contains all of our playing cards
deck_graphic = pygame.image.load('deck_purple.png').convert()
deck_graphic.set_colorkey(( 255, 0, 255)) #purple

#specify surface dimensions for each playing card
card_size_x = 167.5
card_size_y = 243
cropped_card_graphic = pygame.Surface((card_size_x,card_size_y))


#specify number of cards for given classification
deck_size = 52
suit_size = 4
rank_size = 13

card_increment = 0
rank_increment = 0


fpsTime = pygame.time.Clock()

#specify xy coordinates for card 
card_x = 0
card_y = 0

suit = 0
rank = 0
    
while True:
    panda = pygame.image.load('pandaplaying.jpg').convert()
    screen.blit(panda,(screen_size_x/5.4,screen_size_y/5))
    #event cases
    for event in pygame.event.get():
        pass
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            card_x,card_y = pygame.mouse.get_pos()
            
   
    #print every suit..
    suit = card_increment%suit_size

    
    card_increment += 1
    screen.blit(deck_graphic,(card_x,card_y),
                                (rank*card_size_x,suit*card_size_y,card_size_x,card_size_y))
    #..for every rank
    if card_increment%suit_size == 0:
        rank_increment += 1
        rank = rank_increment%rank_size
    
               
                
    fpsTime.tick(FPS)
    pygame.display.flip( )
    

if __name__ == '__main__':
    pass