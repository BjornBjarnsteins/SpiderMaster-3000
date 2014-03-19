from SpiderDeck import SpiderDeck
from SpiderCard import SpiderCard
from SpiderStack import SpiderStack

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
    #      the first 4 stacks contain 6 cards, 5 of them are hidden
    #      the remaining 6 stacks contain 5 cards, 4 of which are hidden
    #      every stack is of type SpiderStack and every card is of type SpiderCard
    def __init__(self,number_of_suits):
        decklength = 104

        self.deck = SpiderDeck(number_of_suits)
        self.deck.shuffle()
        #deck has been shuffled
                
        #initially, 54 cards are dealt to the table
        #The cards are dealt in 10 piles
        num_of_piles = 10
        self.stacks = [0]*num_of_piles
        #first four piles will have 6 cards, the remaining six will have 5 cards
        for i in range(0,num_of_piles):
            #stacks contains i stacks
            if i < 4:
                stack_six_cards = self.remove_n_items(6,self.deck)
                self.stacks[i] = SpiderStack(stack_six_cards,5)
            else:
                stack_five_cards = self.remove_n_items(5,self.deck)                
                self.stacks[i] = SpiderStack(stack_five_cards,4)
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
    #Obsolete:
    #def move(self,n,a,b):
    #    if not self.stacks[a].isEmpty() and self.isLegalMove(n,a,b):
    #        self.stacks[b].add(self.stacks[a].remove(n))

    #use:  s.deal()
    #post: 10 cards have been removed from the hidden pile (deck) and have been distributed 
    #      and put on top of every stack in stacks face up
    def deal(self):
        num_cards_removed = 10
        cards_dealt = self.remove_n_items(num_cards_removed, self.deck)
        #cards_dealt is a list that contains 10 cards of type SpiderCard
        for index in range(0,num_cards_removed):
            toAdd = SpiderStack([cards_dealt.pop()],0)
            self.stacks[index].add(toAdd)
            #one revealed card has been put on top of stacks[index]
            #one hidden card has been removed from cards_dealt
    
    #use: s = game.getStacks()
    #post: s is an array of the ten stacks in the instance 'game' of spidersolitaire.
    def getStacks(self):
        return self.stacks
    
    #use: b = s.isLegal(n,a,b)
    #pre: n,a and b are positive integers
    #post:b=True if it is legal to move the last n cards of stack a to stack b.
    #     'Legal' is if the card to be moved is next in the card sequence to the card it's being moved onto. 
    #     They do not need to be of the same suit.
    def isLegalMove(self, stackOff, stackOn):
        if stackOn.isEmpty():
            return True       
        topCard = stackOff.cards[0] #card being moved onto another card
        bottomCard = stackOn.cards[-1] #card to be moved upon
        topRank = topCard.rank
        bottomRank = bottomCard.rank
        
        if(topRank == bottomRank-1):
            return True
        else:
            return False
    
    #use: b = game.isLegalPickup(s,j)    
    #pre: j is integer from 0 to length of stack-1.
    #post: b = True if the cards from j (counted from 0) in the stack s down to the last card 
    #      are of the same suit and in correct number sequence, from largest number to smallest.
    #     else, b = False.
    def isLegalPickup(self, stack, j):
        n = len(stack)-j
        return self.inSuit(stack,n)
    
    #use: b = s.isSuit(stack,n)
    #pre: stack is a stack object, a and n are positive integers
    #post: b = True if the bottom n cards of stack form a whole suit, else b = False.
    def inSuit(self, Stack, n):
        mainSuit = Stack.cards[-1].getSuitNo()
        oldRank = Stack.cards[-1].rank
        for i in range(2,n+1):
            suit = Stack.cards[-i].getSuitNo()
            newRank = Stack.cards[-i].rank
            if(suit != mainSuit or newRank != oldRank+1):
                return False  
            oldRank = newRank
        return True
             
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