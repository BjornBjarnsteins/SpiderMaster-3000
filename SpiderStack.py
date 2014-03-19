#The SpiderStack will be for each of the 10 columns in play. 
#It will have the following traits:
#Number of cards in the Stack
#Number of hidden cards in the deck (those will be at the front of the array, we'll use the class variable variable 'hidden' for this)
#location on the board as well as length
from SpiderCard import SpiderCard

class SpiderStack:
    '''
    Data invariants:
    
    cards:   a list/stack of SpiderCard objects
            
    hidden:  the number of cards turned face down in this stack
    
    '''
    
    # Use:  stack = SpiderStack(size, hidden)
    # Pre:  cards is a list of SpiderCard objects, hidden is the number of turned down cards
    # Post: stack is a stack of SpiderCard objects
    def __init__(self, cards, hidden):
        self.cards = cards
        self.hidden = hidden

    # Use:  lenght = len(stack)
    # Post: length is the size of the stack
    def __len__(self):
        return len(self.cards)
        
    # Use:  b = stack.isEmpty()
    # Post: b is True if stack is empty, False otherwise
    def isEmpty(self):
        return len(self.cards) == 0
    
    # Use:  b = stack.hasHidden()
    # Post: b is True if stack has any hidden cards, False otherwise
    def hasHidden(self):
        return self.hidden >= 1
    
    # Use:  b = stack.hasVisible()
    # Post: b is True if stack has visible cards, False otherwise
    def hasVisible(self):
        return self.hidden != len(self.cards)

    # Use:  stack.flip()
    # Post: the number of hidden cards in the stack is decreased by one
    def flip(self):
        if not self.isEmpty() and not self.hasVisible():
            self.hidden -= 1

    # Use:  stack1.add(stack2)
    # Pre:  stack2 is a CardStack object
    # Post: stack2 has been put on top of stack1
    def add(self, stack):
        self.cards = self.cards + stack.cards

    # Use:  removedStack = stack.remove(n)
    # Pre:  n is an integer, n > 0
    # Post: the top n cards of stack have been removed. removedStack is a new stack object containing
    #       the cards that were removed.
    def remove(self, n):
        removedCards = self.cards[len(self)-n:]
        self.cards = self.cards[:len(self)-n]
        return SpiderStack(removedCards, 0)

    def getStack(self):
        return [self.cards, self.hidden]
        
        
if __name__=="__main__":
    c1 = SpiderCard('H', 1)
    c2 = SpiderCard('H', 2)
    c3 = SpiderCard('H', 3)
    cardList = [c1, c2, c3]
    stack = SpiderStack(cardList, 2)
    print len(stack)
    print stack.hasHidden()
    print stack.isEmpty()
    stack2 = stack.remove(1)
    print stack.hasVisible()
    print len(stack2)
    stack.add(stack)
    print len(stack)
    stack.flip()
    print stack.hasVisible()