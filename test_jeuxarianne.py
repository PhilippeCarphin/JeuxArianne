import unittest
import jeuxarianne

class TestJABoard(unittest.TestCase):

    def setUp(self):
        self.test_board = jeuxarianne.JABoard()
        self.bigger_board = jeuxarianne.JABoard((8,8))

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

    def play_game(self, board=None):
        if not board:
            board = self.test_board
        board.play_edge(((0,0),(0,1)), 0)

        board.play_edge(((0,0),(1,0)), 1)

        board.play_edge(((0,1),(1,1)), 0)

        board.play_edge(((1,0),(1,1)), 1)
        board.play_edge(((1,1),(1,2)), 1)

        board.play_edge(((1,1),(2,1)), 0)

        board.play_edge(((0,1),(0,2)), 1)

        board.play_edge(((0,2),(1,2)), 0)
        board.play_edge(((1,2),(2,2)), 0)

        board.play_edge(((2,1),(2,2)), 1)
        board.play_edge(((2,0),(2,1)), 1)

        # board.play_edge(((1,0),(2,0)), 0)

    def test_str(self):
        self.play_game()

        print(str(self.test_board))

    def test_different_size(self):
        self.play_game(self.bigger_board)
        # self.assertEqual(self.bigger_board.score, 0)
        pass

    def test_get_value(self):
        self.play_game(self.test_board)
        print("get_value(): ", self.test_board.get_value())

    def test_get_value_empty_board(self):
        self.test_board.play_edge(((0,0),(0,1)), 0)

        self.test_board.play_edge(((0,0),(1,0)), 1)

        self.test_board.play_edge(((0,1),(1,1)), 0)
        self.test_board.play_edge(((1,1),(2,1)), 0)

        self.test_board.play_edge(((0,1),(0,2)), 1)

        self.test_board.play_edge(((0,2),(1,2)), 0)
        self.test_board.play_edge(((1,2),(2,2)), 0)

        self.test_board.play_edge(((2,1),(2,2)), 1)
        self.test_board.play_edge(((2,0),(2,1)), 1)

        # board.play_edge(((1,0),(2,0)), 0)

    def test_str(self):
        self.play_game()

        print(str(self.test_board))

    def test_different_size(self):
        self.play_game(self.bigger_board)
        # self.assertEqual(self.bigger_board.score, 0)
        pass

    def test_get_value(self):
        self.play_game(self.test_board)
        print("get_value(): ", self.test_board.get_value())

    def test_get_value_empty_board(self):
        self.test_board.play_edge(((0,0),(0,1)), 0)

        self.test_board.play_edge(((0,0),(1,0)), 1)

        self.test_board.play_edge(((0,1),(1,1)), 0)
        print(self.test_board.get_value())


        print(self.test_board.get_value())



