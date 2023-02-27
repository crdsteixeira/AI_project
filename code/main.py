import pygame
import sys
from pygame.locals import *
from copy import deepcopy
from Board import Board
from Player import Human, AI
from Game import Game
import config

# Initialize pygame and the main clock
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window
WINDOW_SURF = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption('Fanorona')

# Set up the fonts
SMALL_FONT = pygame.font.Font(None, 10)
BIG_FONT = pygame.font.Font(None, 15)

# Draw Initial Screen
game = Game(WINDOW_SURF, main_clock, BIG_FONT)
options = []
while len(options) < 4:
    options = game.draw_initial_screen()
    print(options)

# Draw Board
game_mode = options['mode']
algorithm = options['algorithm']
board_size = [int(n) for n in options['size'].split() if n != 'X']
difficulty = options['difficulty']
tokens = options['token']

print(tokens)
print(board_size)

board = Board(board_size[0], board_size[1])
grid = board.get_new_grid()

if game_mode == "Computer vs Human":
    player_1 = Human(config.WHITE if tokens == 'White' else config.BLACK, board, difficulty, algorithm)
    player_2 = AI(config.BLACK if tokens == 'White' else config.WHITE, board, difficulty, algorithm)
    player_2.initialize_ai_player()
elif game_mode == "Human vs Human":
    player_1 = Human(config.WHITE if tokens == 'White' else config.BLACK, board, difficulty, algorithm)
    player_2 = Human(config.BLACK if tokens == 'White' else config.WHITE, board, difficulty, algorithm)
elif game_mode == "Computer vs Computer":
    player_1 = AI(config.WHITE if tokens == 'White' else config.BLACK, board, difficulty, algorithm)
    player_1.initialize_ai_player()
    player_2 = AI(config.BLACK if tokens == 'White' else config.WHITE, board, difficulty, algorithm)
    player_2.initialize_ai_player()
else:
    sys.exit(0)

turn = config.WHITE
while True:
    game.draw_grid(grid, board)
    if player_1.token_color == turn:
        grid = player_1.make_turn(grid, game)
    elif player_2.token_color == turn:
        grid = player_2.make_turn(grid, game)
    turn = config.WHITE if turn == config.BLACK else config.BLACK
