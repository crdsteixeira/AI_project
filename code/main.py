import pygame
import sys
from pygame.locals import *
from copy import deepcopy
from Board import Board
from Player import Human, AI
from Game import Game
import config
import stats
import re

# Initialize pygame and the main clock
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window
WINDOW_SURF = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption('Fanorona')

# Set up the fonts
SMALL_FONT = pygame.font.Font(None, 10)
BIG_FONT = pygame.font.Font(None, 20)
EXTRA_BIG_FONT = pygame.font.Font(None, 35)

# Draw Initial Screen
game = Game(WINDOW_SURF, main_clock, BIG_FONT)
options = []
while len(options) < 4:
    options = game.draw_initial_screen()

# Draw Board
chosen_player_1 = options['player_1']
chosen_player_2 = options['player_2']
board_size = [int(s) for s in re.findall(r'-?\d+\.?\d*', options['size'])]  # find only numbers from the string
difficulty = options['difficulty']

board = Board(board_size[0], board_size[1])
grid = board.get_new_grid()

if chosen_player_1 == "Human":
    player_1 = Human(config.WHITE, board, difficulty)
    ## hint button
else:
    player_1 = AI(config.WHITE, board, difficulty, chosen_player_1)
    player_1.initialize_ai_player()

if chosen_player_2 == "Human":
    player_2 = Human(config.BLACK, board, difficulty)
    ## hint button
else:
    player_2 = AI(config.BLACK, board, difficulty, chosen_player_2)
    player_2.initialize_ai_player()

# board = Board(9, 5)
# grid = board.get_new_grid()
#
# player_1 = AI(config.WHITE, board, difficulty='Medium', algorithm='Minimax_AlphaBeta')
# player_1.initialize_ai_player()
# player_2 = AI(config.BLACK, board, difficulty='Medium', algorithm='Monte_Carlo_TS')
# player_2.initialize_ai_player()

turn = config.WHITE
tic = pygame.time.get_ticks()  # initiate timer

while grid:
    game.draw_grid(grid, board)

    if player_1.token_color == turn:
        grid = player_1.make_turn(grid, game)

    elif player_2.token_color == turn:
        grid = player_2.make_turn(grid, game)

    turn = config.WHITE if turn == config.BLACK else config.BLACK

# send info to export file 
stats.options_prepare_row(options)
toc = pygame.time.get_ticks()  # finalize timer
timee = (toc - tic) / 1000  # save time in seconds
stats.duration(timee)  # save time in seconds
stats.export_results()

# show screen with game_results
game.show_results(options)