import pygame
import sys
from pygame.locals import *
from copy import deepcopy
from Board import Board
#import Player
from Game import Screen
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
screen = Screen(WINDOW_SURF, main_clock, BIG_FONT)
options = []
while len(options) < 4:
    options = screen.draw_initial_screen()
    print(options)

# Draw Board
game_mode = options['mode']
board_size = [int(n) for n in options['size'].split() if n != 'X']
difficulty = options['difficulty']
token = options['token']

print(board_size)


board = Board(board_size[0], board_size[1])
grid = board.get_new_grid()

while True:
    screen.draw_grid(grid, board)