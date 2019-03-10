import unittest
import jeuxarianne

class TestJABoard(unittest.TestCase):

    def setUp(self):
        self.test_board = jeuxarianne.JABoard()

    def test_in_board(self):
        self.assertTrue(self.test_board.in_board((2,1)))
        self.assertFalse(self.test_board.in_board((2,3)))

    def test_edge_is_legal(self):
        self.assertTrue(self.test_board.edge_is_legal(((0,0),(0,1))))
        self.assertFalse(self.test_board.edge_is_legal(((0,0),(1,1))))
        self.assertFalse(self.test_board.edge_is_legal(((0,0),(1,3))))

    def test_square_is_surrounded(self):
        self.assertRaises(Exception, self.test_board.square_is_surrounded, (2,2))

    def test_play_edge(self):
        self.test_board.play_edge(((0,0),(0,1)), 0)
        self.assertRaises(AssertionError, self.test_board.play_edge, ((0,0),(0,1)), 0)

    def test_str(self):
        print(str(self.test_board))
