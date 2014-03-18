import unittest
from pygame.locals import *
from SpiderCard import *


class Test(unittest.TestCase):


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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()