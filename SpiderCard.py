#Defines a card to be used in the solitaire.
import pygame
import sys

class Card:
    # the size of the cards on deck.png
    card_size_x = 168
    card_size_y = 243
    
    # Use:  card = Card(suit, rank)
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
    
    # Use:  n = card.getSuitNo()
    # Post: n is the ID of the suit of the card    
    def getSuitNo(self):
        return {'C': 0,
                'D': 1,
                'H': 2,
                'S': 3}.get(self.suit, self.suit)
                
    def __str__(self):
        return self.suit + str(self.rank)
    
    # Use:  cardSurface = card.getPicture()
    # Post: cardSurface is a Surface object with the picture of the card
#     def getPicture(self, screen):
#         card_sheet = pygame.image.load('deck.png')
#         card_template = pygame.Surface((self.card_size_x, self.card_size_y))
#         card_graphic = screen.blit(card_sheet, (0,0), 
#                                          ((self.rank-1)*self.card_size_x, self.getSuitNo()*self.card_size_y, self.card_size_x, self.card_size_y))
#         return card_graphic

if __name__=="__main__":
    # Tests getSuitNo method
    C1 = Card('C', 1)
    D4 = Card('D', 4)
    print C1.getSuitNo()
    print D4.getSuitNo()
    
    # Tests the getPicture method
#     screen = pygame.display.set_mode((Card.card_size_x, Card.card_size_y))
#     
#     while True:
#         screen.blit(C1.getPicture(screen))
#Has a method to an image for the card icon.