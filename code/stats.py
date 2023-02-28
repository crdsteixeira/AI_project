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
 
def options_prepare_row (options_list):
    player1 = options_list['player_1']
    player2 = options_list['player_2']
    board_size = options_list['size']
    difficulty = options_list['difficulty']
    
    global options
    options = [player1, player2 , board_size, difficulty]
    
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

    with open('Scores.csv', 'a', newline = '') as scores_file:
        my_writer = csv.writer(scores_file, delimiter = ',')
        my_writer.writerow(row)
        scores_file.close()