"""
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

main.py: Main control logic

Functions:

- draw_option
- draw_all_options
- draw_readytostart
- draw_initial_screen
- draw_grid
- draw_circle
- translate_grid_to_pixel_coord
- get_grid_clicked
- mave_move
- show_results
- check for draw
"""

import copy

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

else:
    player_1 = AI(config.WHITE, board, difficulty, chosen_player_1)
    player_1.initialize_ai_player()

if chosen_player_2 == "Human":
    player_2 = Human(config.BLACK, board, difficulty)

else:
    player_2 = AI(config.BLACK, board, difficulty, chosen_player_2)
    player_2.initialize_ai_player()

# board = Board(9, 5)

# boards = [(3, 3), (5, 5), (9, 5)]
# difficulties = ['Easy', 'Medium', 'Hard']
# algorithms = ['Minimax', 'Minimax_AlphaBeta', 'Monte_Carlo_TS']
# players = [(config.WHITE, config.BLACK), (config.BLACK, config.WHITE) ]
#
# for size in boards:
#     for level_1 in difficulties:
#         for level_2 in difficulties:
#             for alg_1 in algorithms:
#                 for alg_2 in algorithms:
#                     for order in players:
#                         # Initialize pygame and the main clock
#                         pygame.init()
#                         main_clock = pygame.time.Clock()
#
#                         # Set up the window
#                         WINDOW_SURF = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
#                         pygame.display.set_caption('Fanorona')
#
#                         # Set up the fonts
#                         SMALL_FONT = pygame.font.Font(None, 10)
#                         BIG_FONT = pygame.font.Font(None, 20)
#                         EXTRA_BIG_FONT = pygame.font.Font(None, 35)
#                         game = Game(WINDOW_SURF, main_clock, BIG_FONT)
#
#                         options = {'player_1': alg_1,
#                                    'player_2': alg_2,
#                                    'size': [size[0], size[1]],
#                                    'difficulty': (level_1, level_2)
#                                    }
#                         game.selected_options = options
#                         print(options)
#                         board = Board(size[0], size[1])
#                         grid = board.get_new_grid()
#                         player_1 = AI(order[0], board, difficulty=level_1, algorithm=alg_1)
#                         player_1.initialize_ai_player()
#                         player_2 = AI(order[1], board, difficulty=level_2, algorithm=alg_2)
#                         player_2.initialize_ai_player()


turn = config.WHITE
tic = pygame.time.get_ticks()  # initiate timer
previous_states = []

while grid:
    game.draw_grid(grid, board)
    previous_states.append((copy.deepcopy(grid), turn))

    if player_1.token_color == turn:
        grid = player_1.make_turn(grid, game)
    elif player_2.token_color == turn:
        grid = player_2.make_turn(grid, game)

    turn = config.WHITE if turn == config.BLACK else config.BLACK
    if grid:
        # print(grid)
        if game.check_for_draw(grid, turn, previous_states, board, player_1, player_2):
            stats.winner_str('Draw')
            break
    else:
        if turn == config.WHITE:
            # Export results to csv file
            stats.winner_str('Player_1')
        else:
            stats.winner_str('Player_2')

# send info to export file
stats.options_prepare_row(options, previous_states)
toc = pygame.time.get_ticks()  # finalize timer
timee = (toc - tic) / 1000  # save time in seconds
stats.duration(timee)  # save time in seconds
stats.export_results()

# show screen with game_results
game.show_results(options)
