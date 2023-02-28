"""
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

Board.py : This class represents the game board, and has methods to place and move pieces, check for valid moves,
and print the board.

Functions:
- get_new_grid(...)
- get_movable_token_information(...)
- is_within_grid(...)
- clean_table(...)

"""


from numpy import size
import pygame
import sys
from pygame.locals import *
# from main import *
# from Player import *
from copy import deepcopy

import config

# colors
WHITE = config.WHITE
BLACK = config.BLACK
GREEN = config.GREEN
RED = config.RED
EMPTY = config.EMPTY

WINDOW_WIDTH = config.WINDOW_WIDTH  # width of the program's window, in pixels
WINDOW_HEIGHT = config.WINDOW_HEIGHT  # height in pixels


class Board:

    def __init__(self, cols, rows):
        self.GRID_SIZE = 50  # size of the beads
        self.GRID_COLS = cols  # how many columns of grid on the game board
        self.GRID_ROWS = rows  # how many rows of spaces on the game board

    def get_new_grid(self):
        """Returns a 2-dimensional array of token information.
        The first/second array index means column/row number that count from zero.
        Each token information is a hash table containing its token color and
        displacements of all adjacent grid positions.
        """

        grid = []
        for i in range(self.GRID_COLS):
            grid.append([])

        for coloumn in grid:
            for i in range(self.GRID_ROWS):
                coloumn.append({'token_color': EMPTY,
                                'displacements': []})

        # initialize grid positions with different displacements of
        # all adjacent grid positions

        # 3 X 3
        if self.GRID_COLS == 3:

            # first column

            grid[0][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (1, 1)]:
                grid[0][0]['displacements'].append(displacement)

            grid[0][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (0, -1)]:
                grid[0][1]['displacements'].append(displacement)

            grid[0][2]['token_color'] = WHITE
            for displacement in [(1, -1), (1, 0), (0, -1)]:
                grid[0][2]['displacements'].append(displacement)

            # second column

            grid[1][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[1][0]['displacements'].append(displacement)

            grid[1][1]['token_color'] = EMPTY
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[1][1]['displacements'].append(displacement)

            grid[1][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[1][2]['displacements'].append(displacement)

            # third column

            grid[2][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1)]:
                grid[2][0]['displacements'].append(displacement)

            grid[2][1]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, 1), (0, -1)]:
                grid[2][1]['displacements'].append(displacement)

            grid[2][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (-1, -1)]:
                grid[2][2]['displacements'].append(displacement)

        # 5 X 5
        if self.GRID_COLS == 5:

            # first column

            grid[0][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (1, 1)]:
                grid[0][0]['displacements'].append(displacement)

            grid[0][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (0, -1)]:
                grid[0][1]['displacements'].append(displacement)

            grid[0][2]['token_color'] = BLACK
            for displacement in [(1, -1), (1, 0), (0, -1), (0, 1), (1, 1)]:
                grid[0][2]['displacements'].append(displacement)

            grid[0][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (0, -1)]:
                grid[0][3]['displacements'].append(displacement)

            grid[0][4]['token_color'] = WHITE
            for displacement in [(1, -1), (1, 0), (0, -1)]:
                grid[0][4]['displacements'].append(displacement)

            # second column

            grid[1][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[1][0]['displacements'].append(displacement)

            grid[1][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[1][1]['displacements'].append(displacement)

            grid[1][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[1][2]['displacements'].append(displacement)

            grid[1][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[1][3]['displacements'].append(displacement)

            grid[1][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[1][4]['displacements'].append(displacement)

            # third column

            grid[2][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1), (1, 0), (1, 1)]:
                grid[2][0]['displacements'].append(displacement)

            grid[2][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[2][1]['displacements'].append(displacement)

            grid[2][2]['token_color'] = EMPTY
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[2][2]['displacements'].append(displacement)

            grid[2][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[2][3]['displacements'].append(displacement)

            grid[2][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)]:
                grid[2][4]['displacements'].append(displacement)

            # fourth column

            grid[3][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[3][0]['displacements'].append(displacement)

            grid[3][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[3][1]['displacements'].append(displacement)

            grid[3][2]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[3][2]['displacements'].append(displacement)

            grid[3][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[3][3]['displacements'].append(displacement)

            grid[3][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[3][4]['displacements'].append(displacement)

            # fifth column

            grid[4][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1)]:
                grid[4][0]['displacements'].append(displacement)

            grid[4][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (0, -1)]:
                grid[4][1]['displacements'].append(displacement)

            grid[4][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (-1, -1), (0, 1), (-1, 1)]:
                grid[4][2]['displacements'].append(displacement)

            grid[4][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, 1), (0, -1)]:
                grid[4][3]['displacements'].append(displacement)

            grid[4][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (-1, -1)]:
                grid[4][4]['displacements'].append(displacement)

        # 5 X 9
        if self.GRID_COLS == 9:

            # first column

            grid[0][0]['token_color'] = BLACK
            for displacement in [(1, 0), (1, 1), (0, 1)]:
                grid[0][0]['displacements'].append(displacement)

            grid[0][1]['token_color'] = BLACK
            for displacement in [ (0, -1), (1, 0), (0, 1)]:
                grid[0][1]['displacements'].append(displacement)

            grid[0][2]['token_color'] = BLACK
            for displacement in [(1, -1), (1, 0), (0, -1), (0, 1), (1, 1)]:
                grid[0][2]['displacements'].append(displacement)

            grid[0][3]['token_color'] = WHITE
            for displacement in [(0, -1), (1, 0), (0, 1)]:
                grid[0][3]['displacements'].append(displacement)

            grid[0][4]['token_color'] = WHITE
            for displacement in [(1, -1), (1, 0), (0, -1)]:
                grid[0][4]['displacements'].append(displacement)

            # second column

            grid[1][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[1][0]['displacements'].append(displacement)

            grid[1][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[1][1]['displacements'].append(displacement)

            grid[1][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[1][2]['displacements'].append(displacement)

            grid[1][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[1][3]['displacements'].append(displacement)

            grid[1][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[1][4]['displacements'].append(displacement)

            # third column

            grid[2][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1), (1, 0), (1, 1)]:
                grid[2][0]['displacements'].append(displacement)

            grid[2][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[2][1]['displacements'].append(displacement)

            grid[2][2]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[2][2]['displacements'].append(displacement)

            grid[2][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[2][3]['displacements'].append(displacement)

            grid[2][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)]:
                grid[2][4]['displacements'].append(displacement)

            # fourth column

            grid[3][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[3][0]['displacements'].append(displacement)

            grid[3][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[3][1]['displacements'].append(displacement)

            grid[3][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[3][2]['displacements'].append(displacement)

            grid[3][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[3][3]['displacements'].append(displacement)

            grid[3][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[3][4]['displacements'].append(displacement)

            # fifth column

            grid[4][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1), (1, 0), (1, 1)]:
                grid[4][0]['displacements'].append(displacement)

            grid[4][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[4][1]['displacements'].append(displacement)

            grid[4][2]['token_color'] = EMPTY
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[4][2]['displacements'].append(displacement)

            grid[4][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[4][3]['displacements'].append(displacement)

            grid[4][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)]:
                grid[4][4]['displacements'].append(displacement)

            # sixth column

            grid[5][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[5][0]['displacements'].append(displacement)

            grid[5][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[5][1]['displacements'].append(displacement)

            grid[5][2]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[5][2]['displacements'].append(displacement)

            grid[5][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[5][3]['displacements'].append(displacement)

            grid[5][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[5][4]['displacements'].append(displacement)

            # seventh column

            grid[6][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1), (1, 0), (1, 1)]:
                grid[6][0]['displacements'].append(displacement)

            grid[6][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[6][1]['displacements'].append(displacement)

            grid[6][2]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[6][2]['displacements'].append(displacement)

            grid[6][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[6][3]['displacements'].append(displacement)

            grid[6][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)]:
                grid[6][4]['displacements'].append(displacement)

            # eighth column

            grid[7][0]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0)]:
                grid[7][0]['displacements'].append(displacement)

            grid[7][1]['token_color'] = BLACK
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[7][1]['displacements'].append(displacement)

            grid[7][2]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                grid[7][2]['displacements'].append(displacement)

            grid[7][3]['token_color'] = WHITE
            for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1),
                                 (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                grid[7][3]['displacements'].append(displacement)

            grid[7][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (1, 0)]:
                grid[7][4]['displacements'].append(displacement)

            # ninth column

            grid[8][0]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (-1, 1)]:
                grid[8][0]['displacements'].append(displacement)

            grid[8][1]['token_color'] = BLACK
            for displacement in [(-1, 0), (0, 1), (0, -1)]:
                grid[8][1]['displacements'].append(displacement)

            grid[8][2]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (-1, -1), (0, 1), (-1, 1)]:
                grid[8][2]['displacements'].append(displacement)

            grid[8][3]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, 1), (0, -1)]:
                grid[8][3]['displacements'].append(displacement)

            grid[8][4]['token_color'] = WHITE
            for displacement in [(-1, 0), (0, -1), (-1, -1)]:
                grid[8][4]['displacements'].append(displacement)

        print(grid)
        return grid

    def get_movable_token_information(self, token_color, grid, is_prompt_bi_direct_capture=True):
        """returns a hash table that hashes each movable token
        coordinate to its own hash table consisting of each accordingly available
        empty grid coordinates to move hashing to its move type.
        """
        capture_move_table = {}
        paika_move_table = {}
        has_capture = False  # a flag shows which table to return

        # GRID_COLS = len(grid)
        # GRID_ROWS = int(size(grid)/GRID_COLS)

        for column in range(self.GRID_COLS):
            for row in range(self.GRID_ROWS):
                if grid[column][row]['token_color'] == token_color:
                    paika_move_table[(column, row)] = {}
                    capture_move_table[(column, row)] = {}
                    for (delta_x, delta_y) in grid[column][row]['displacements']:

                        # when a token's neighbor is EMPTY, it at least eligible for Paika move
                        # only after a token in Paika list, it will be test for what kind of
                        # capture it fits within the boundary of grid.

                        if grid[column + delta_x][row + delta_y]['token_color'] == EMPTY:
                            paika_move_table[(column, row)][(column + delta_x, row + delta_y)] = 'paika'

                            if self.is_within_grid(column + 2 * delta_x, row + 2 * delta_y) and \
                                    grid[column + 2 * delta_x][row + 2 * delta_y]['token_color'] \
                                    != token_color and \
                                    grid[column + 2 * delta_x][row + 2 * delta_y]['token_color'] \
                                    != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                    = 'approach'
                                has_capture = True

                                if is_prompt_bi_direct_capture and \
                                        self.is_within_grid(column - delta_x, row - delta_y) and \
                                        grid[column - delta_x][row - delta_y]['token_color'] \
                                        != token_color and \
                                        grid[column - delta_x][row - delta_y] \
                                                ['token_color'] != EMPTY:
                                    capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                        = 'bi-direction'

                            elif self.is_within_grid(column - delta_x, row - delta_y) and \
                                    grid[column - delta_x][row - delta_y]['token_color'] \
                                    != token_color and \
                                    grid[column - delta_x][row - delta_y]['token_color'] \
                                    != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                    = 'withdraw'
                                has_capture = True

        if has_capture:
            result_table = self.clean_table(capture_move_table)
            print(('get from movable token information\ncapture table  ', result_table, '\n'))
            return result_table

        else:
            result_table = self.clean_table(paika_move_table)
            print(('get from movable token information\npaika table  ', result_table, '\n'))
            return result_table

    def is_within_grid(self, x, y):
        return x >= 0 and x < self.GRID_COLS and y >= 0 and y < self.GRID_ROWS

    def clean_table(self, move_table):
        # return a cleaned move table that only consists of valid move.
        new_table = {k: v for k, v in move_table.items() if v != {}}
        return new_table
