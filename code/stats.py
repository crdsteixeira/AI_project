"""
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

This file receives parameters, organizes them, and saves them into the Script.csv file (existing) in the same directory.

Cols in the correct order in Script.py: 
  Player1,
  Player2,
  Board_Size,
  Difficulty,
  TODO total_nodes_player_1
  TODO total_nodes_player_2
  Game_Time(s),
  Winner
"""
import csv
import config
import pygame
import sys

#import main


def options_prepare_row(options_list, previous_states):
    player1 = options_list['player_1']
    player2 = options_list['player_2']
    board_size = options_list['size']
    difficulty = options_list['difficulty']
    len_play = len(previous_states)

    global options
    options = [player1, player2, board_size, difficulty, len_play]


def winner_str(winner_str):
    global winner
    winner = winner_str
    print(winner)


def duration(timee):
    global time_dur
    time_dur = str(timee)
    print(time_dur)


def export_results():
    row = options
    row.append(time_dur)
    row.append(winner)

    with open('Scores.csv', 'a', newline='') as scores_file:
        my_writer = csv.writer(scores_file, delimiter=',')
        my_writer.writerow(row)
        scores_file.close()

# show results

# def show_game_results(BIG_FONT, draw=False):
#     #global total_node_generated
#     #global depth_of_game_tree
#     #print ("\n\nfinally,  level is, nodes are ", depth_of_game_tree, '\n\n', total_node_generated)
#     if draw:
#         # text_surf = BIG_FONT.render('The game is draw', True, config.BLACK)
#         # text_rect = text_surf.get_rect()
#         # text_rect.center = (int(config.WINDOW_COLS*0.5), int(config.WINDOW_ROWS*0.875))
#         print("The game is a draw!")
#
#         # while True:
#         #     for event in pygame.event.get():
#         #         if event.type == pygame.QUIT:
#         #             pygame.quit()
#         #             sys.exit()
#
#         #     pygame.WINDOW_SURF.blit(text_surf, text_rect)
#         #     pygame.main_clock.tick(config.FPS)
#         #     pygame.display.update()
#
#     else:
#         text_surf = BIG_FONT.render('The game is over', True, config.BLACK)
#         text_rect = text_surf.get_rect()
#         text_rect.center = (int(config.WINDOW_COLS*0.5), int(config.WINDOW_ROWS*0.875))
#
#         winner_surf = BIG_FONT.render(winner + '  Win!', True, config.BLACK)
#         winner_rect = winner_surf.get_rect()
#         winner_rect.center = (int(config.WINDOW_COLS*0.25), int(config.WINDOW_ROWS*0.9375))
#
#         # loser_surf = BIG_FONT.render(loser_str + '  Lose~~', True, config.BLACK)
#         # loser_rect = loser_surf.get_rect()
#         # loser_rect.center = (int(config.WINDOW_COLS*0.75), int(config.WINDOW_ROWS*0.9375))
#     print("Winner: ", winner_str)
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         self.WINDOW_SURF.blit(text_surf, text_rect)
#         self.WINDOW_SURF.blit(winner_surf, winner_rect)
#         #self.WINDOW_SURF.blit(loser_surf, loser_rect)
#         #show_statistics()
#         self.main_clock.tick(config.FPS)
#         pygame.display.update()
