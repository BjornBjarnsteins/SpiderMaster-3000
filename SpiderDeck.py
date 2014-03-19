#SpiderDeck needs to define a deck of 104 (2*52) cards with the following traits:
#Number of suits: 1 (spades), 2 (hearts, spades) or all 4.
#In the case of only one suit, the deck will be put together of the sequence of Ace of Spades, 2, 3, 4,...,King of Spades 8 times
#In the case of two suits, the deck will be put together of the sequence of Ace of Spades, 2, 3, 4, ...., King of Spades 4 times and likewise for the Heart sequence 4 times
#In the case of all four suits, each sequence will appear 2 times.

#All in all: It will always take 8 complete sequences to win the game, no matter what suit or difficulty
from SpiderCard import SpiderCard
import random

class SpiderDeck:
    '''
    Data invariants:
    
    decklist: a list of SpiderCard objects.
            
    suits:    the suits present in the deck, either 1, 2, or 4
    
    '''
    
    # Use:  deck = SpiderDeck(n)
    # Pre:  n is a number, 1, 2 or 4
    # Post: deck is a deck of cards containing n suits and 104 cards
    def __init__(self, suitNo):
        # decklist er listi af Card hlutum
        self.decklist = []
        self.suits = []
        if suitNo == 1:
            suits = ['S']
        elif suitNo == 2:
            suits = ['S', 'H']
        elif suitNo == 4:
            suits = ['S', 'H', 'D', 'C']
            
        for n in range(0, 8/suitNo):
            for suit in suits:
                for rank in range(1, 14):
                    self.decklist.append(SpiderCard(suit, rank))
            
    # Use:  SpiderDeck.shuffle()
    # Post: SpiderDeck is shuffled        
    def shuffle(self):
        random.shuffle(self.decklist)
        
    # Use:  cards = SpiderDeck.remove()
    # Post: the card on the top of the deck has been removed
    def remove(self):
        return self.decklist.pop()
    
    def __str__(self):
        card_string = ''
        for cards in self.decklist:
            card_string = card_string + cards.suit + str(cards.rank) + ' '
            if cards.rank == 13:
                card_string = card_string + '\n'
        return card_string
                    
if __name__=="__main__":
    #Testing functions
    deck = SpiderDeck(1)
    deck.shuffle()
    for c in deck.decklist:
        print c
    
    print
    print
    
    print len(deck.decklist)
    
    print deck.remove()
    for n in range(0, 8):
        print deck.remove()