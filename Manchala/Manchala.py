import numpy as np
import math
import copy
import pygame
from random import randint
from Player import Player, Random_Player
from Board import Board
  

ellipse_width_block = 40
ellipse_height_block = 100
width_spacing = 20
height_spacing = 50
screen_width = 500
screen_height = 400
piece_width = 10
piece_height = 10
pieces_per_location = {}
for i in range(2):
    for j in range(7):
        pieces_per_location[(i, j)] = []


def play_game(players):
    board = Board()
    print("---Starting game---")
    board.print_board()
    
    turn = 0
    while board.game_end() == False:
        again = True
        while again == True and board.game_end() == False:
            index = players[turn].pick_move(board)
            (board, again) = players[turn].move(board, index)
            board.print_board()
        turn = (turn + 1) % 2
    
    print("WINNER IS", board.get_winner())


def fill_board_ui(pygame, screen):
    screen.fill((255, 255, 255))
    cup_color = (242, 158, 68)
    # store: height = 300, width = 40
    # cup: height = 100, width = 40
    # width space between cups = 20
    # screen width: 40 * 8 + 20 * 9
    # screen height: 400
    pygame.draw.ellipse(screen, cup_color, (width_spacing, height_spacing, ellipse_width_block, ellipse_height_block * 3))
    pygame.draw.ellipse(screen, cup_color, (screen_width - width_spacing - ellipse_width_block, height_spacing, ellipse_width_block, ellipse_height_block * 3))
    for i in range(6):
        for j in range(2):
            pygame.draw.ellipse(screen, cup_color, (width_spacing + ellipse_width_block + width_spacing + (i * (width_spacing + ellipse_width_block)), height_spacing + (j * (2*height_spacing + ellipse_height_block)), ellipse_width_block, ellipse_height_block))

def convert_start_point(row, col):
    height_start = None
    width_start = None
    if row == 0 and col == 0:
        height_start = height_spacing
        width_start = width_spacing
    elif row == 1 and col == 6:
        height_start = height_spacing
        width_start = screen_width - width_spacing - ellipse_width_block
    elif row == 0:
        height_start = height_spacing
        width_start = width_spacing + ellipse_width_block + width_spacing + ((col -1)* (width_spacing + ellipse_width_block))
    else:
        height_start = height_spacing + (2*height_spacing + ellipse_height_block)
        width_start = width_spacing + ellipse_width_block + width_spacing + ((col) * (width_spacing + ellipse_width_block))
    return (height_start, width_start)

def fill_pieces_ui(pygame, screen, row, col, pieces):
    (height_start, width_start) = convert_start_point(row, col)
    height_end = height_start + (ellipse_height_block * 3 if (row == 0 and col == 0) or (row == 1 and col == 6) else ellipse_height_block)
    width_end = width_start + ellipse_width_block
    for piece in range(pieces):
        randheight = randint(height_start + 25, height_end - 25)
        randwidth = randint(width_start + 15, width_end - 15)
        piece_color = list(np.random.choice(range(256), size=3))
        ellipse = (piece_color, (randwidth, randheight, piece_width, piece_height))
        pygame.draw.ellipse(screen, ellipse[0], ellipse[1])
        pieces_per_location[(row, col)].append(ellipse)

def print_pieces():
    p_0 = []
    p_1 = []
    for key in pieces_per_location.keys():
        if key[0] == 0:
            p_0.append(len(pieces_per_location[key]))
        else:
            p_1.append(len(pieces_per_location[key]))
    print(p_0)
    print(p_1)

def fix_location(piece_removed, row, col):
    (height_start, width_start) = convert_start_point(row, col)
    height_end = height_start + (ellipse_height_block * 3 if (row == 0 and col == 0) or (row == 1 and col == 6) else ellipse_height_block)
    width_end = width_start + ellipse_width_block
    randheight = randint(height_start + 25, height_end - 25)
    randwidth = randint(width_start + 15, width_end - 15)
    piece_removed = (piece_removed[0], (randwidth, randheight, piece_width, piece_height))
    return piece_removed

def fill_cup_ui(pygame, screen, board, old_board, start_row, start_col):
    piece_width = 10
    piece_height = 10
    if old_board == None:
        for row in range(2):
            for col in range(7):
                if board.cups[row][col].pieces != 0:
                    fill_pieces_ui(pygame, screen, row, col, board.cups[row][col].pieces)
    else:
        print("BEFORE!---------------------------------------------------", start_row, start_col, old_board.cups[start_row][start_col].pieces, board.cups[start_row][start_col].pieces )
        # print_pieces()
        # old_board.print_board()
        # board.print_board()
        ellipses_movement = {}
        for i in range(10):
            ellipses_movement[i] = []
        for row in range(2):
            for col in range(7):
                if old_board.cups[row][col].pieces != board.cups[row][col].pieces:
                    # have to move pieces since the number of pieces do not match
                    if (start_row == row and start_col == col) == False:
                        num_movement = board.cups[row][col].pieces - old_board.cups[row][col].pieces
                        moved = 0
                        # pieces already there
                        for piece in pieces_per_location[(row, col)]:
                            for i in range(10):
                                ellipses_movement[i].append(piece)
                        # new pieces going there
                        while moved < num_movement:
                            # old board had less pieces so need to move to here from starting position
                            piece_removed = pieces_per_location[(start_row, start_col)].pop(0)
                            old_coordinates = (piece_removed[0], (piece_removed[1][0], piece_removed[1][1], piece_removed[1][2], piece_removed[1][3]))
                            piece_removed = fix_location(piece_removed, row, col)
                            new_coordinates = (piece_removed[0], (piece_removed[1][0], piece_removed[1][1], piece_removed[1][2], piece_removed[1][3]))
                            pieces_per_location[(row, col)].append(piece_removed)
                            # movement for the piece that is going to the new spot
                            width_movement = new_coordinates[1][0] - old_coordinates[1][0]
                            height_movement = new_coordinates[1][1] - old_coordinates[1][1]
                            for i in range(10):
                                new_width_spot = old_coordinates[1][0] + i*(width_movement/10)
                                new_height_spot = old_coordinates[1][1] + i*(height_movement/10)
                                new_ellipse = (piece_removed[0], (new_width_spot, new_height_spot, piece_removed[1][2], piece_removed[1][3]))
                                ellipses_movement[i].append(new_ellipse)
                            moved += 1
                else:
                    # can keep these pieces are they are currently
                    for piece in pieces_per_location[(row, col)]:
                        for i in range(10):
                            ellipses_movement[i].append(piece)
        # show the pieces aalready at the starting location
        for piece in pieces_per_location[(start_row, start_col)]:
            for i in range(10):
                ellipses_movement[i].append(piece)

        t = 0
        while t < 10:
            fill_board_ui(pygame, screen)
            for movement in ellipses_movement[t]:
                pygame.draw.ellipse(screen, movement[0], movement[1])
            t += 1
            pygame.display.flip()
            pygame.time.delay(30) 
        print_pieces()
        print("AFTER!---------------------------------------------------")


def play_game_with_ui(players):
    board = Board()
    print("---Starting game---")
    board.print_board()

    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.flip()
    fill_board_ui(pygame, screen)
    fill_cup_ui(pygame, screen, board, None, None, None)

    turn = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while board.game_end() == False:
            again = True
            while again == True and board.game_end() == False:
                old_board = copy.deepcopy(board)
                index = players[turn].pick_move(board)
                (board, again) = players[turn].move(board, index)
                fill_board_ui(pygame, screen)
                fill_cup_ui(pygame, screen, board, old_board, turn, index)
                pygame.display.flip()
                pygame.time.delay(300) 
            turn = (turn + 1) % 2

if __name__  == "__main__":
    players = [Random_Player(0), Random_Player(1)]
    play_game_with_ui(players)