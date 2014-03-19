import unittest
import random
from pygame.locals import *
from SpiderCard import *
from SpiderStack import *
from SpiderDeck import *
from SpiderSolitaire import *


class TestSpiderCard(unittest.TestCase):

    def setUp(self):
        self.card1 = SpiderCard('H', 3)


    def test_getSuitNo(self):
        suitNo = self.card1.getSuitNo()
        self.assertEqual(suitNo, 2)

    def test_getImage(self):
        pygame.init()
        pygame.display.set_mode((int(SpiderCard.card_size_x), SpiderCard.card_size_y))
        self.testSurface = self.card1.getImage()
        self.assertEqual(self.testSurface.get_width(), int(self.card1.card_size_x))

class TestSpiderStack(unittest.TestCase):

    #before we initialize the SpiderStack object for testing we need a 
    #list of SpiderCard objects as input
    cards = [SpiderCard("H",1),SpiderCard("S",2)]
    hidden = 1
    
    stack = SpiderStack(cards, hidden)
    stack2 = SpiderStack(cards,hidden)
    
    def test_isEmpty(self):
        self.assertFalse(self.stack2.isEmpty())
    
    def test_hasHidden(self):
        self.assertTrue(self.stack.hasHidden())
    
    def test_hasVisible(self):
        self.assertTrue(self.stack2.hasVisible())
    
    #flip decreases number of hidden cards by one if there are no revealed cards at top of the stack
    def test_flip(self):
        self.stack2.flip()
        self.assertTrue(self.stack2.hasHidden()) #produces an error, should be false
        self.stack2.remove(1)
        self.stack2.flip()
        self.assertFalse(self.stack2.hasHidden())
    
    def test_add(self):
        #add stack on top of itself
        length = len(self.stack)*2
        stack_to_add = self.stack #number of cards = 2
        self.stack.add(self.stack)
        self.assertEqual(len(self.stack),length)
    
    def test_remove(self):
        cards_removed = len(self.stack)
        self.stack.remove(cards_removed)
        self.assertTrue(self.stack.isEmpty())
        
    def test_getStack(self):
        pass
        
class TestSpiderSolitaire(unittest.TestCase):
    
    number_of_suits = 1
    solitaire = SpiderSolitaire(number_of_suits)
    
    def test_deal(self):
        hidden_cards = 50
        cards_dealt = 10
        num_times_to_deal = hidden_cards/cards_dealt
        for i in range(0,num_times_to_deal):
            try:
                self.solitaire.deal()
            except KeyError, ex:
                print "KeyError: " + ex
    
    def test_getStacks(self):
        stacks = self.solitaire.getStacks()
        self.assertEqual(self.solitaire.stacks,stacks)
        
    def test_remove_n_functions(self):
        pass 
    
    def test_miscellaneous(self):
        
        C1 = SpiderCard('H', 7)
        C2 = SpiderCard('H', 6)
        C3 = SpiderCard('S', 5)
        C4 = SpiderCard('H', 4)
        C5 = SpiderCard('H', 3)
        
        B1 = SpiderCard('S', 8)
        testStack = SpiderStack([C1, C2, C3, C4, C5], 0)
        stackOff = SpiderStack([C1, C2],0)
        stackOn = SpiderStack([B1],0) 
        
        self.assertTrue(self.solitaire.inSuit(testStack, 2))
        self.assertFalse(self.solitaire.inSuit(testStack, 3))
        self.assertTrue(self.solitaire.isLegalPickup(testStack, 3))
        self.assertFalse(self.solitaire.isLegalPickup(testStack,2))
        self.assertTrue(self.solitaire.isLegalMove(stackOff, stackOn))

    
class TestSpiderDeck(unittest.TestCase):

    deck1 = SpiderDeck(1)
    deck2 = SpiderDeck(2)
    deck4 = SpiderDeck(4)
    
    len1 = len(deck1.decklist)
    len2 = len(deck2.decklist)
    len3 = len(deck4.decklist)
    
    def test_init(self):
        # Checks if all decks are equally long
        self.assertEqual(self.len1, self.len2)
        self.assertEqual(self.len2, self.len3)
        self.assertEqual(self.len1, self.len3)
    
    def test_shuffle1(self):
        self.deck1.shuffle()
        self.assertEqual(len(self.deck1.decklist), self.len1)
        
    def test_shuffle2(self):
        card1 = self.deck1.remove()
        self.assertIsInstance(card1, SpiderCard)
        self.assertEqual(len(self.deck1.decklist), self.len1-1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
