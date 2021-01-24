import numpy as np
import math
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

def convert_start_point(screen, row, col):
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
    (height_start, width_start) = convert_start_point(screen, row, col)
    height_end = height_start + (ellipse_height_block * 3 if (row == 0 and col == 0) or (row == 1 and col == 6) else ellipse_height_block)
    width_end = width_start + ellipse_width_block
    for piece in range(pieces):
        randheight = randint(height_start + 25, height_end - 25)
        randwidth = randint(width_start + 15, width_end - 15)
        piece_color = list(np.random.choice(range(256), size=3))
        pygame.draw.ellipse(screen, piece_color, (randwidth, randheight, piece_width, piece_height))

def fill_cup_ui(pygame, screen, board):
    piece_width = 10
    piece_height = 10
    for row in range(2):
        for col in range(7):
            if board.cups[row][col].pieces != 0:
                fill_pieces_ui(pygame, screen, row, col, board.cups[row][col].pieces)
    
def play_game_with_ui(players):
    board = Board()
    print("---Starting game---")
    board.print_board()

    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.flip()

    turn = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while board.game_end() == False:
            again = True
            while again == True and board.game_end() == False:
                index = players[turn].pick_move(board)
                (board, again) = players[turn].move(board, index)
                fill_board_ui(pygame, screen)
                fill_cup_ui(pygame, screen, board)
                pygame.display.flip()
                pygame.time.delay(300) 
            turn = (turn + 1) % 2


if __name__  == "__main__":
    players = [Random_Player(0), Random_Player(1)]
    play_game_with_ui(players)