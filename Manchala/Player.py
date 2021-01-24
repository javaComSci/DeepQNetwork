from random import randint
from Board import Board

class Player:
    def __init__(self, player_num):
        self.player_num = player_num
                
    def next_spot(self, board, row, col):
        if col == 1 and row == 0 and self.player_num == 1:
            col = 0
            row = 1
        elif col == 5 and row == 1 and self.player_num == 0:
            col = 6
            row = 0
        elif col == 0 and row == 0:
            row += 1
        elif col == 6 and row == 1:
            row -= 1
        elif row == 1:
            col += 1
        elif row == 0:
            col -= 1
        return (row, col)
            
    def move(self, board, start_index):
        if self.player_num == 1:
            assert(start_index != 6)
        if self.player_num == 0:
            assert(start_index != 0)
        pieces_to_move = board.cups[self.player_num][start_index].pieces
        board.cups[self.player_num][start_index].pieces = 0
        (row, col) = self.next_spot(board, self.player_num, start_index)
        while pieces_to_move > 0:
            board.cups[row][col].pieces += 1
            pieces_to_move -= 1
            if pieces_to_move == 0 and self.player_num == row:
                return (board, True)
            (row, col) = self.next_spot(board, row, col)
        return (board, False)
    
    def pick_move(self, board):
        raise NotImplementedError("Overriden method")

class Random_Player(Player):
    def pick_move(self, board):
        r = -1
        if self.player_num == 0:
            r = randint(1, 6)
            while board.cups[self.player_num][r].pieces == 0:
                r = randint(1, 6)
        else:
            r = randint(0, 5)
            while board.cups[self.player_num][r].pieces == 0:
                r = randint(0, 5)
        return r