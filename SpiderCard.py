#Defines a card to be used in the solitaire.
import pygame
import sys
from pygame.locals import *

card_x = 0
card_y = 0

class SpiderCard:
    '''
    Data invariants:
    
    suit:   the suit of the card, one of the following: 'H', 'D', 'C', 'S'
            
    rank:   the rank of the card, 1 <= rank <= 13
    
    '''
    # the size of the cards on deck.png
    card_size_x = 167.5
    card_size_y = 243
    # Use:  card = SpiderCard(suit, rank)
    # Pre:  suit is a single upper-case character:
    #            H: Heart
    #            D: Diamond
    #            C: Clubs
    #            S: Spade
    #       rank is an integer, 1-13
    # Post: card is a playing card with suit suit and rank rank
    def __init__(self, suit ,rank):
        self.suit = suit
        self.rank = rank
    
    # Use:  n = SpiderCard.getSuitNo()
    # Post: n is the ID of the suit of the card    
    def getSuitNo(self):
        return {'C': 0,
                'D': 1,
                'H': 2,
                'S': 3}.get(self.suit, self.suit)
                
    def __str__(self):
        return self.suit + str(self.rank)
    
    # Use:  cardSurface = SpiderCard.getPicture(hidden=False)
    # Pre:  hidden is an optional boolean variable for whether the card is facing up or down,
    #       deck_graphic is an Image object, a deck of cards graphic
    # Post: cardSurface is a Surface object with the picture of the card
    def getImage(self, deck_graphic,hidden=False):
        card_template = pygame.Surface((self.card_size_x, self.card_size_y))  
        if hidden:
            card_template.blit(deck_graphic,(0,0),
                                (2*self.card_size_x,4*self.card_size_y,self.card_size_x,self.card_size_y))
        else:
            card_template.blit(deck_graphic,(0,0),
                                ((self.rank-1)*self.card_size_x,self.getSuitNo()*self.card_size_y,self.card_size_x,self.card_size_y))
        return card_template

if __name__=="__main__":
    # Tests getSuitNo method
    C1 = SpiderCard('S', 13)
    D4 = SpiderCard('D', 4)
    print C1.getSuitNo()
    print D4.getSuitNo()

    #Tests the getPicture method
    screen = pygame.display.set_mode((int(SpiderCard.card_size_x), SpiderCard.card_size_y))
    deck_graphic = pygame.image.load('deck.png').convert()
    while True:
        screen.blit(C1.getImage(deck_graphic), (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
                card_x,card_y = pygame.mouse.get_pos()
