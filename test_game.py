from game import Game
import unittest

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()


    def test_board(self):
        self.assertEqual(self.game.board, [['-','-','-'],['-','-','-'],['-','-','-']])


    def test_is_board_full(self):
        self.assertEqual(self.game.is_board_full(), False)
        self.game.board = [['X','O','X'],\
                            ['O','X','O'],\
                            ['X','O','X']]
        self.assertEqual(self.game.is_board_full(), True)


    def test_get_all_valid_moves(self):
        self.game.board = [['X','O','X'],\
                            ['O','X','O'],\
                            ['X','O','X']]
        self.assertEqual(self.game.get_all_valid_moves(), [])

        self.game.board = [['X','O','X'],\
                            ['O','X','O'],\
                            ['X','O','-']]
        self.assertEqual(self.game.get_all_valid_moves(), [[2, 2]])


    def test_reset(self):
        self.game.board = [['X','O','X'],\
                            ['O','X','O'],\
                            ['X','O','-']]
        self.game.reset()
        self.assertEqual(self.game.board, [['-','-','-'],\
                                            ['-','-','-'],\
                                            ['-','-','-']])
    

    def test_undo_move(self):
        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','-']]
        self.game.moves_history = [[2,1]]
        self.game.undo_move()
        self.assertEqual(self.game.board, [['X','O','X'], \
                                            ['O','X','O'], \
                                            ['X','-','-']])


    def test_check_play_ended(self):
        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','-']]
        self.game.moves_history = [[2, 0]]
        self.assertEqual(self.game.check_play_ended(), "X won!")

        self.game.board = [['X','O','X'], \
                            ['O','X','X'], \
                            ['O','X','O']]
        self.assertEqual(self.game.check_play_ended(), "It's a tie!")
    
        self.game.board = [['O','X','X'], \
                            ['O','X','O'], \
                            ['O','O','X']]
        self.game.moves_history = [[2, 0]]
        self.assertEqual(self.game.check_play_ended(), "O won!")


    def test_get_corners(self):
        self.assertEqual(self.game.get_corners(), [[0,0],[0,2],[2,0],[2,2]])


    def test_get_edges(self):
        self.assertEqual(self.game.get_edges(), [[0,1],[1,0],[1,2],[2,1]])


    def test_get_valid_corners(self):
        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','-']]
        self.assertEqual(self.game.get_valid_corners(), [[2,2]])

        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','X']]
        self.assertEqual(self.game.get_valid_corners(), [])


    def test_is_won(self):
        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','-']]
        self.game.moves_history = [[1, 1]]
        self.assertEqual(self.game.is_won('X'), True)

        self.game.board = [['X','O','X'], \
                            ['O','X','O'], \
                            ['X','O','-']]
        self.game.moves_history = [[1, 1]]
        self.assertEqual(self.game.is_won('O'), False)

    def test_counter_two_edges_strategy(self):

        self.game.board = [  ['-','X','-'], \
                            ['X','O','-'], \
                            ['-','-','-']]
        self.game.moves_history = [[0, 1], [1,1],[1,0]]
        self.assertTrue(self.game.are_cells_adjacent([0,1],[1,0]))
        self.assertTrue(self.game.are_opponents_cells_adjacent([0,1],[1,0], 'O'))    
        self.assertEqual(self.game.opposite_corner([0,1],[1,0]), [2,2])
        self.assertEqual(self.game.adjacent_corners([0,1],[1,0]), [[0,0],[0,2],[2,0]])
        self.assertIn(self.game.random_adjacent_corner([0,1],[1,0]), [[0,0],[0,2],[2,0]])

        self.game.board = [  ['-','X','-'], \
                        ['-','O','X'], \
                        ['-','-','-']]
        self.game.moves_history = [[0,1],[1,1],[1,2]]
        self.assertTrue(self.game.are_opponents_cells_adjacent([0,1],[1,2], 'O'))
        self.assertEqual(self.game.opposite_corner([0,1],[1,2]), [2,0])
        self.assertEqual(self.game.adjacent_corners([0,1],[1,2]), [[0,0],[0,2],[2,2]])
        self.assertIn(self.game.random_adjacent_corner([0,1],[1,2]), [[0,0],[0,2],[2,2]])


if __name__ == '__main__':
    unittest.main()

    
