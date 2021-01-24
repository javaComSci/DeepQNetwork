from Cup import Cup

class Board:
    def __init__(self):
        p1_cups = []
        p2_cups = []
        for i in range(6):
            p1_cups.append(Cup(4, 0))
            p2_cups.append(Cup(4, 1))
        p1_cups.insert(0, Cup(0, 0))
        p2_cups.append(Cup(0, 1))
        self.cups = []
        self.cups.append(p1_cups)
        self.cups.append(p2_cups)
    
    def check_row_0(self):
        ended = True
        for i in range(7):
            if i != 0 and self.cups[0][i].pieces != 0:
                ended = False
                break
        return ended

    def check_row_1(self):
        ended = True
        for i in range(7):
            if i != 6 and self.cups[1][i].pieces != 0:
                ended = False
                break
        return ended
    
    def game_end(self):
        ended = self.check_row_0() or self.check_row_1()
        return ended
    
    def get_winner(self):
        if self.check_row_0():
            return 0
        return 1
        
    def print_board(self):
        print("--------------------------")
        for i in range(2):
            print("Player", i, list(map(lambda cup: cup.pieces, self.cups[i])))
        print("--------------------------")