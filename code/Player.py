import pygame
import random
from main import *


class Player:
    def __init__(self, token_color, grid_height, grid_width):
        self.token_color = token_color
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width

    def is_within_grid(self, x, y):
        return 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT

    def clean_table(self, move_table):
        """return a cleaned move table that only consists of valid move.
        """
        new_table = {k: v for k, v in move_table.items() if v != {}}
        return new_table

    def get_movable_token_information(self, grid, is_prompt_bi_direct_capture=True):
        """returns a hash table that hashes each movable token
        coordinate to its own hash table consisting of each accordingly available
        empty grid coordinates to move hashing to its move type.
        """
        capture_move_table = {}
        paika_move_table = {}
        has_capture = False  # a flag shows which table to return

        for column in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if grid[column][row]['token_color'] == self.token_color:
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
                                    != self.token_color and \
                                    grid[column + 2 * delta_x][row + 2 * delta_y]['token_color'] \
                                    != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                    = 'approach'
                                has_capture = True

                                if is_prompt_bi_direct_capture and \
                                        self.is_within_grid(column - delta_x, row - delta_y) and \
                                        grid[column - delta_x][row - delta_y]['token_color'] \
                                        != self.token_color and \
                                        grid[column - delta_x][row - delta_y] \
                                                ['token_color'] != EMPTY:
                                    capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                        = 'bi-direction'

                            elif self.is_within_grid(column - delta_x, row - delta_y) and \
                                    grid[column - delta_x][row - delta_y]['token_color'] \
                                    != self.token_color and \
                                    grid[column - delta_x][row - delta_y]['token_color'] \
                                    != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)] \
                                    = 'withdraw'
                                has_capture = True

        if has_capture:
            result_table = self.clean_table(capture_move_table)
            print('get from movable token information\ncapture table  ', result_table, '\n')
            return result_table

        else:
            result_table = self.clean_table(paika_move_table)
            print('get from movable token information\npaika table  ', result_table, '\n')
            return result_table

    def get_all_tokens_on_grid(self, grid):
        """Returns a list of all tokens on the grid that match this player's token_color."""
        tokens = []
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                if grid[col][row]['token_color'] == self.token_color:
                    tokens.append((col, row))
        return tokens

    def get_movable_positions_for_token(self, token, grid):
        """Returns a list of positions where the token at the given column and row can move to."""
        movable_positions = []
        for direction in DIRECTIONS:
            new_col, new_row = token[0] + direction[0], token[1] + direction[1]
            if not (0 <= new_col < self.GRID_WIDTH and 0 <= new_row < self.GRID_HEIGHT):
                continue
            if grid[new_col][new_row]['token_color'] != EMPTY:
                continue
            movable_positions.append((new_col, new_row))
        return movable_positions

    def make_move(self, token, position, grid):
        """Updates the given grid with the given move."""
        new_grid = copy.deepcopy(grid)
        new_grid[token[0]][token[1]]['token_color'] = EMPTY
        new_grid[position[0]][position[1]]['token_color'] = self.token_color
        return new_grid


class AIPlayer(Player):
    def __init__(self, token_color, difficulty):
        super().__init__(token_color)
        self.difficulty = difficulty

    def get_next_move(self, grid):
        if self.difficulty == "easy":
            return self._get_random_move(grid)
        elif self.difficulty == "medium":
            return self._get_minimax_move(grid, depth=3)
        else:  # self.difficulty == "hard"
            return self._get_minimax_move(grid, depth=5)

    def _get_random_move(self, grid):
        tokens = self.get_all_tokens_on_grid(grid)
        while True:
            random_token = random.choice(tokens)
            movable_positions = self.get_movable_positions_for_token(random_token, grid)
            if movable_positions:
                return (random_token, random.choice(movable_positions))

    def _get_minimax_move(self, grid, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0:
            return None, None, self._evaluate_board(grid)

        if maximizing_player:
            best_move = None
            best_value = float('-inf')
            tokens = self.get_all_tokens_on_grid(grid)
            for token in tokens:
                movable_positions = self.get_movable_positions_for_token(token, grid)
                for position in movable_positions:
                    new_grid = copy.deepcopy(grid)
                    new_grid = self.make_move(token, position, new_grid)
                    _, _, value = self._get_minimax_move(new_grid, depth-1, alpha, beta, False)
                    if value > best_value:
                        best_move = (token, position)
                        best_value = value
                    alpha = max(alpha, best_value)
                    if alpha >= beta:
                        break  # beta cutoff
            return best_move[0], best_move[1], best_value

        else:  # minimizing player
            worst_move = None
            worst_value = float('inf')
            tokens = self.get_all_opponent_tokens_on_grid(grid)
            for token in tokens:
                movable_positions = self.get_movable_positions_for_token(token, grid)
                for position in movable_positions:
                    new_grid = copy.deepcopy(grid)
                    new_grid = self.make_move(token, position, new_grid)
                    _, _, value = self._get_minimax_move(new_grid, depth-1, alpha, beta, True)
                    if value < worst_value:
                        worst_move = (token, position)
                        worst_value = value
                    beta = min(beta, worst_value)
                    if beta <= alpha:
                        break  # alpha cutoff
            return worst_move[0], worst_move[1], worst_value

    def _evaluate_board(self, grid):
        opponent_color = self.get_opponent_token_color()
        own_tokens = self.get_all_tokens_on_grid(grid)
        opponent_tokens = self.get_all_opponent_tokens_on_grid(grid)
        own_token_count = len(own_tokens)
        opponent_token_count = len(opponent_tokens)
        return own_token_count - opponent_token_count