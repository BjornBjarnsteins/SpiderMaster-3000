from SpiderDeck import SpiderDeck
from SpiderCard import Card
from SpiderStack import CardStack

#The game (from wikipedia)
#The main purpose of the game is to remove all cards 
#from the table, assembling them in the tableau before removing them. 
#Initially, 54 cards are dealt to the tableau in ten piles, face down 
#except for the top cards. The tableau piles build down by rank, and in-suit 
#sequences can be moved together. The 50 remaining cards can be dealt to the 
#tableau ten at a time when none of the piles are empty.

class SpiderSolitaire:
    '''
    Data invariants:
    
    stacks: contains 10 stacks/piles of cards
            these stacks contain all the cards that have been dealt
            
    deck:   contains all the cards that have not yet been dealt
            it can be thought of as the hidden pile
    
    '''
    #use:  s = SpiderSolitaire(number_of_suits)
    #pre:  number_of_suits is an integer 1,2 or 4
    #post: s now contains 10 stacks 
    #      the first 4 stacks contain 5 cards, 4 of them are hidden
    #      the remaining 6 stacks contain 6 cards, 5 of which are hidden
    #      every stack is of type CardStack and every card is of type Card
    def __init__(self,number_of_suits):
        decklength = 104

        self.deck = SpiderDeck(number_of_suits)
        self.deck.shuffle()
        #deck has been shuffled
                
        #initially, 54 cards are dealt to the table
        #The cards are dealt in 10 piles
        num_of_piles = 10
        self.stacks = [0]*num_of_piles
        #first four piles will have 5 cards, the remaining six will have 4 cards
        for i in range(0,num_of_piles):
            #stacks contains i stacks
            if i < 4:
                stack_six_cards = self.remove_n_items(6,self.deck)
                self.stacks[i] = CardStack(stack_six_cards,5)
            else:
                stack_five_cards = self.remove_n_items(5,self.deck)                
                self.stacks[i] = CardStack(stack_five_cards,4)
        #54 cards have been dealt
        #deck now contains decklength-54 = 104-54 = 100 cards
        
    #pre:  n is a positive integer, deck is a SpiderDeck
    #post: removes and returns the n foremost cards from deck, 
	#	   the cards are returned in a list
    def remove_n_items(self,n,deck):
        new_list = [0]*n
        for i in range(0,n):
            try:
                new_list[i] = deck.remove()
            except KeyError:
                print "You can't remove a card from an empty deck"
        return new_list
    
    #use: s.move(n,a,b)
    #pre; n, a and b are positive integers
    #post: the n bottom cards have been moved from position a to b in stacks
    def move(n,a,b):
        if not self.stacks[a].isEmpty():
            self.stacks[b].add(self.stacks[a].remove(n))

    #use:  s.deal()
    #post: 10 cards have been removed from the hidden pile (deck) and have been distributed 
    #      and put on top of every stack in stacks face up
    def deal(self):
        num_cards_removed = 10
        cards_dealt = self.remove_n_items(num_cards_removed, self.deck)
        #cards_dealt is a list that contains 10 cards of type Card
        for index in range(0,num_cards_removed):
            stacks[index].add(cards_dealt.pop())
            #one revealed card has been put on top of stacks[index]
            #one hidden card has been removed from cards_dealt
            
        
#vika 2
#def calcScore()

# Vika 2:
#for storing and loading high scores into txt file:
#def store()
#def load()


if __name__ == '__main__':
    s = SpiderSolitaire(1)
    print len(s.deck.decklist)
    for SpiderCard in s.stacks:
        for j in SpiderCard.cards:
            print(j),
        print