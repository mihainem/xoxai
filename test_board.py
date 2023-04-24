import board
import unittest

class TestBoard(unittest.TestCase):
    def test_board(self):
        board = board.Board()
        self.assertEqual(board.get_board(), [['-','-','-'],['-','-','-'],['-','-','-']])

    def test_is_board_full(self):
        board = board.Board()
        self.assertEqual(board.is_board_full(), False)

    def test_is_board_full(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','X']]
        self.assertEqual(board.is_board_full(), True)

    def test_get_all_valid_moves(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','X']]
        self.assertEqual(board.get_all_valid_moves(), [])

    def test_get_all_valid_moves(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        self.assertEqual(board.get_all_valid_moves(), [2, 2])

    def test_reset(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        board.reset()
        self.assertEqual(board.get_board(), [['-','-','-'],['-','-','-'],['-','-','-']])
    
    def test_undo_move(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        board.moves_history = [[2,1]]
        board.undo_move()
        self.assertEqual(board.get_board(), [['X','O','X'],['O','X','O'],['X','-','-']])

    def test_check_play_ended(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        self.assertEqual(board.check_play_ended(), "X won!")

    def test_check_play_ended(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','X'],['O','X','O']]
        self.assertEqual(board.check_play_ended(), "It's a tie!")

    def test_check_play_ended(self):
        board = board.Board()
        board.board = [['O','X','X'],['O','X','O'],['O','O','X']]
        self.assertEqual(board.check_play_ended(), "O won!")

    def test_get_corners(self):
        board = board.Board()
        self.assertEqual(board.get_corners(), [[0,0],[0,2],[2,0],[2,2]])

    def test_get_edges(self):
        board = board.Board()
        self.assertEqual(board.get_edges(), [[0,1],[1,0],[1,2],[2,1]])

    def test_get_valid_corners(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        self.assertEqual(board.get_valid_corners(), [[2,2]])

    def test_get_valid_corners(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','X']]
        self.assertEqual(board.get_valid_corners(), [])

    def test_is_won(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        self.assertEqual(board.is_won('X'), True)

    def test_is_won(self):
        board = board.Board()
        board.board = [['X','O','X'],['O','X','O'],['X','O','-']]
        board.moves_history = [[]]
        self.assertEqual(board.is_won('O'), False)


    
