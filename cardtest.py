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
    
    stack = SpiderStack(cards,hidden)
    
    def test_isEmpty(self):
        self.assertFalse(self.stack.isEmpty())
    
    def test_hasHidden(self):
        self.assertTrue(self.stack.hasHidden())
    
    def test_hasVisible(self):
        self.assertTrue(self.stack.hasVisible())
    
    #flip decreases number of hidden cards by one
    def test_flip(self):
        self.stack.flip()
        self.assertEqual(self.stack.hasHidden(), False) #produces an error, should be false
    
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
        hidden_cards = 100
        cards_dealt = 10
        num_times_to_deal = hidden_cards /cards_dealt
        for i in range(0,num_times_to_deal):
            try:
                self.solitaire.deal()
            except KeyError, ex:
                print "KeyError: " + ex
    
    def test_move(self):
        pass 
    
    def test_getStacks(self):
        stacks = self.solitaire.getStacks()
        self.assertEqual(self.solitaire.stacks,stacks)
        
    def test_remove_n_functions(self):
        pass 
    
    def test_miscellaneous(self):
        #some random tests
        cards_to_move = 2
        pos_a = 1
        pos_b = 5
        self.solitaire.move(cards_to_move,pos_a,pos_b)
        
        random_num = random.randint(0,len(self.solitaire.stack)-1)
        self.solitaire.isLegalMove(self.solitaire.stack,random_num)
        
        random_num = random.randint(0,len(self.solitaire.stack)-1)
        self.solitaire.isLegalPickup(self.solitaire.stack,random_num)
        
        bottom_n_cards = 3
        self.solitaire.isSuit(self.solitaire.stack,bottom_n_cards)
        self.fail("something went wrong")
        
    
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
    
    def test_shuffle(self):
        self.deck1.shuffle()
        self.assertEqual(len(deck1.decklist), len1)
        
    def test_shuffle(self):
        card1 = deck1.remove()
        self.assertIsInstance(card1, SpiderCard)
        self.assertEqual(len(deck1.decklist), len1-1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
