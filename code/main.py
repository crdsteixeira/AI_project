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
board_size = [int(s) for s in re.findall(r'-?\d+\.?\d*', options['size'])] # find only numbers from the string
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
tic = pygame.time.get_ticks() # initiate timer


while grid:
    game.draw_grid(grid, board)

    if player_1.token_color == turn:
        grid = player_1.make_turn(grid, game)
            
    elif player_2.token_color == turn:
        grid = player_2.make_turn(grid, game)
    
    turn = config.WHITE if turn == config.BLACK else config.BLACK

# send info to export file 
stats.options_prepare_row(options)
toc = pygame.time.get_ticks() # finalize timer
timee = (toc-tic)/1000 # save time in seconds
stats.duration(timee) # save time in seconds
stats.export_results()

# show screen with game_results

text_surf = EXTRA_BIG_FONT.render('GAME OVER!', True, config.BLACK)
text_rect = text_surf.get_rect()
text_rect.center = (int(config.WINDOW_WIDTH*0.5), int(config.WINDOW_HEIGHT*0.150))

# find the real loser and winner
winner_str = options[stats.winner.lower()]
if winner_str == 'player_1':
    loser = 'player_2'
else: loser = 'player_1'
loser_str = options[loser]

winner_surf = EXTRA_BIG_FONT.render('Winner: '+ stats.winner + ' (' + winner_str + ')', True, config.GREEN)
winner_rect = winner_surf.get_rect()
winner_rect.center = (int(config.WINDOW_WIDTH*0.5), int(config.WINDOW_HEIGHT*0.875))

loser_surf = EXTRA_BIG_FONT.render('Loser: ' + loser + ' (' + loser_str + ')', True, config.RED)
loser_rect = loser_surf.get_rect()
loser_rect.center = (int(config.WINDOW_WIDTH*0.5), int(config.WINDOW_HEIGHT*0.9375))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WINDOW_SURF.blit(text_surf, text_rect)
    WINDOW_SURF.blit(winner_surf, winner_rect)
    WINDOW_SURF.blit(loser_surf, loser_rect)
    
    main_clock.tick(config.FPS)
    pygame.display.update()
