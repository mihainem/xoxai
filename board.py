import random

class Board:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = [['-' for j in range(cols)] for i in range(rows)] #[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
  
        self.player = "X"
        self.enemy = "O"
        self.history = []
        self.moves_history = []

    def reset(self):
        self.board = [['-' for j in range(self.cols)] for i in range(self.rows)]
        self.moves_history=[]
        
        
    def check_play_ended(self):
        if self.is_won("X"):
            self.history.append("X")
            return "X won!"
        elif self.is_won("O"):
            self.history.append("O")
            return "O won!"
        elif self.is_board_full():
            self.history.append('T')
            return "It's a tie!"
    
    def undo_move(self):
        move = None
        if len(self.moves_history) > 0:
            row, col = move = self.moves_history.pop()
            self.board[row][col] = '-'
        
        return move
   

    def print(self):
        for row in self.board:
            print(row)

    def set(self, board):
        self.board = board

    def is_valid(self, row, col):
        return 0 <= row < self.rows \
            and 0 <= col < self.cols \
            and self.board[row][col] == '-'
    
    def is_board_full(self):
        for row in self.board:
            for col in row:
                if col == '-':
                    return False
        return True
    
    def get_corners(self):
        max_row = self.rows - 1
        max_col = self.cols - 1
        return [[0,0] , [0,max_col], [max_row,0], [max_row,max_col]]
    
    def get_edges(self):
        return [[0,1], [1, 0], [1, 2], [2,1]]
    
    def get_cells(self, cells, valid):
        result = []
        for row, col in cells:
            if self.is_valid(row, col)==valid:
                result.append((row, col))
        return result
    
    def get_valid_corners(self):
        return self.get_cells(self.get_corners(), True)
    
    def get_invalid_corners(self):
        return self.get_cells(self.get_corners(), False)
    
    def get_random_corner(self):
        valid_corners = self.get_valid_corners()
        return random.choice(valid_corners) if (len(valid_corners)> 0) else None
    
    def get_random_valid_move(self):
        valid_moves = self.get_all_valid_moves()
        return random.choice(valid_moves) if (len(valid_moves)> 0) else None
    
    def get_valid_edges(self):
        return self.get_cells(self.get_edges(), True)
    
    def is_won(self, symbol):
        row, col = self.moves_history[-1]
        board = self.board

        if board[row][col] == symbol and (board[row][0] == board[row][1] == board[row][2] == symbol \
            or board[0][col] == board[1][col] == board[2][col] == symbol \
            or board[0][0] == board[1][1] == board[2][2] == symbol \
            or board[0][2] == board[1][1] == board[2][0] == symbol) :
                return True
        return False

    def is_winning_move(self, move, symbol):
        row, col = move
        temp_board = self.board

        c1 = (col + 1) % 3
        c2 = (col + 2) % 3
        r1 = (row + 1) % 3
        r2 = (row + 2) % 3

        print(f"row-col [{row}, {col}] r2-c1 [{r2}, {c1}] r1-c2 [{r1}, {c2}]")
        if self.is_valid(row, col) and (temp_board[row][c1] == temp_board[row][c2] == symbol \
            or temp_board[r1][col] == temp_board[r2][col] == symbol):
                print("found winning line")
                return True
        
        if  self.is_valid(row, col)  and (
            (row == col) and temp_board[r1][r1] == temp_board[r2][r2] == symbol \
            or (row + col == 2) and temp_board[r2][c1] == temp_board[r1][c2] == symbol ) :
                print(f"found wininng  in diagonal ")
                return True
        return False
    
    
    def get_all_valid_moves(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    moves.append([row, col])
        return moves
    
    def make_move(self, move, symbol):
        self.moves_history.append(move)
        row, col = move
        self.board[row][col] = symbol
        return f"{symbol} placed at [{row}, {col}]"

    def best_move(self, symbol):
        if self.is_valid(1, 1):
            return [1, 1]
        
        for move in self.get_all_valid_moves():
            print(f"valid move: {symbol}", move)
            if self.is_winning_move(move, symbol):
                return move
        
        if len(self.get_valid_corners()) == 2 \
            and len(self.get_all_valid_moves()) == 6:
                [r1,c1], [r2, c2] = self.get_invalid_corners()
                print(f"invalid_corners {r1} {c1},  {r2} {c2}")
                if self.board[r1][c1] == self.board[r2][c2] != symbol:
                    return random.choice(self.get_valid_edges())
        
        print(f"no best move found for {symbol}")
        return None
    
    def wrong_move(self, symbol):
        for move in [[0,1], [1,0], [1,2], [2,1]]:
            row, col = move
            if self.is_valid(row, col) and not self.is_winning_move(move, symbol):
                return move
        for move in self.get_valid_corners(): #.get_cells(self.get_corners()):
            row, col = move
            if not self.is_winning_move(move, symbol):
                return move
        return [1, 1]

    def next_best_move(self, player_symbol, enemy_symbol):
        return self.best_move(player_symbol) or self.best_move(enemy_symbol)  or self.get_random_corner() or self.get_random_valid_move()


    def get_hint_move(self):
        return self.next_best_move(self.player, self.enemy)

    def set_player_move(self, move):
        self.make_move(move, self.player)