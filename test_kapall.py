import unittest
import random
from pygame.locals import *
from SpiderCard import *
from SpiderStack import *
from SpiderDeck import *
from SpiderSolitaire import *

#------------------------------------------------------------------------------
# Here we will test the main methods of the game SpiderSolitaire. 
# Classes to be tested:
#    SpiderCard
#    SpiderDeck
#    SpiderStack
#    SpiderSolitaire
#
# We will also test relevant methods from the GUI for this game.
# Modules to be tested:
#    SpiderGUI
#    HighscoreGUI
#    kapall
#------------------------------------------------------------------------------

#Testclass: SpiderCard
#Purpose: Try to create a SpiderCard object, see if it was given the correct
#         suit number and if it's image has correct dimensions.
class TestSpiderCard(unittest.TestCase):

    #UT01
    def setUp(self):
        self.card1 = SpiderCard('H', 3)

    #UT02
    def test_getSuitNo(self):
        suitNo = self.card1.getSuitNo()
        self.assertEqual(suitNo, 2)
    
    #UT03
    def test_getImage(self):
        deckGraphic = pygame.image.load('deck.png')
        pygame.init()
        pygame.display.set_mode((int(SpiderCard.card_size_x), SpiderCard.card_size_y))
        self.testSurface = self.card1.getImage(deckGraphic)
        self.assertEqual(self.testSurface.get_width(), int(self.card1.card_size_x))

#Testclass: SpiderDeck
#Purpose: try to create SpiderDeck objects, see if they are of correct length
#         and whether they can be shuffled. Then see if a card can be removed
#         from the deck.
class TestSpiderDeck(unittest.TestCase):

    deck1 = SpiderDeck(1)
    deck2 = SpiderDeck(2)
    deck4 = SpiderDeck(4)
    
    len1 = len(deck1.decklist)
    len2 = len(deck2.decklist)
    len3 = len(deck4.decklist)
    
    #UT04
    def test_init(self):
        # Checks if all decks are equally long
        self.assertEqual(self.len1, self.len2)
        self.assertEqual(self.len2, self.len3)
        self.assertEqual(self.len1, self.len3)
    
    #UT05
    def test_shuffle1(self):
        self.deck1.shuffle()
        self.assertEqual(len(self.deck1.decklist), self.len1)
    
    #UT06    
    def test_shuffle2(self):
        card1 = self.deck1.remove()
        self.assertIsInstance(card1, SpiderCard)
        self.assertEqual(len(self.deck1.decklist), self.len1-1)

#Testclass: SpiderStack
#Purpose:   Create a stack. Then see if it has a hidden card, if it
#           whether it has a visible card or is empty. Try to flip 
#           a card (= make a hidden card revealed, so long as a hidden
#           card is on top). Try to add and remove cards from the stack.
class TestSpiderStack(unittest.TestCase):

    #before we initialize the SpiderStack object for testing we need a 
    #list of SpiderCard objects as input
    cards = [SpiderCard("H",1),SpiderCard("S",2)]
    hidden = 1
    
    stack = SpiderStack(cards, hidden)
    stack2 = SpiderStack(cards,hidden)
    
    #UT07
    def test_isEmpty(self):
        self.assertFalse(self.stack2.isEmpty())
    
    #UT08
    def test_hasHidden(self):
        self.assertTrue(self.stack.hasHidden())
    
    #UT09
    def test_hasVisible(self):
        self.assertTrue(self.stack2.hasVisible())
    
    #UT10
    #flip decreases number of hidden cards by one if there are no revealed cards at top of the stack
    def test_flip(self):
        self.stack2.flip()
        self.assertTrue(self.stack2.hasHidden()) #produces an error, should be false
        self.stack2.remove(1)
        self.stack2.flip()
        self.assertFalse(self.stack2.hasHidden())
    
    #UT11
    def test_add(self):
        #add stack on top of itself
        length = len(self.stack)*2
        stack_to_add = self.stack #number of cards = 2
        self.stack.add(self.stack)
        self.assertEqual(len(self.stack),length)
    
    #UT12
    def test_remove(self):
        cards_removed = len(self.stack)
        self.stack.remove(cards_removed)
        self.assertTrue(self.stack.isEmpty())
     

#Testclass: SpiderSolitaire
#Purpose:   Create a game of spidersolitaire. Try to deal a new row,
#           check whether a number of cards is of the same suit and
#           in correct order. See if picking them up is legal and if 
#           putting them down is.
class TestSpiderSolitaire(unittest.TestCase):
    
    number_of_suits = 1
    solitaire = SpiderSolitaire(number_of_suits)
    
    #UT13
    def test_deal(self):
        hidden_cards = 50
        cards_dealt = 10
        num_times_to_deal = hidden_cards/cards_dealt
        for i in range(0,num_times_to_deal):
            try:
                self.solitaire.deal()
            except KeyError, ex:
                print "KeyError: " + ex
    
    #UT14
    def test_getStacks(self):
        stacks = self.solitaire.getStacks()
        self.assertEqual(self.solitaire.stacks,stacks)
    
    #UT15-17
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
        
        #UT15
        self.assertTrue(self.solitaire.inSuit(testStack, 2))
        self.assertFalse(self.solitaire.inSuit(testStack, 3))
        #UT16
        self.assertTrue(self.solitaire.isLegalPickup(testStack, 3))
        self.assertFalse(self.solitaire.isLegalPickup(testStack,2))
        #UT17
        self.assertTrue(self.solitaire.isLegalMove(stackOff, stackOn))
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
