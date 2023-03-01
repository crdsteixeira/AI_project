"""
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

Player.py: Controls the different types of player inside the game.

Classes and functions:
- Player
    - wait_a_second()
    - check_movable_token_table()
- Human
    - make_turn()
- AI(Player)
    - initialize_ai_player() TODO: shouldnt this be inside __init__?
    - make_turn()
    - evaluate_current_state()
    - terminal_test()
    - utility()
- Random(Player)
    - play()
- Minimax(AI)
    - play()
    - minimax_search()
    - max_value()
    - min_value()
- MinimaxAlphaBeta(AI)
    - play()
    - alpha_beta_search()
    - max_value()
    - min_value()
- MonteCarloTS(AI)
    - play()
    - mct_search
    - run_iteration
    - tree_policy
- Node(AI)
    - get_untried_actions
    - q
    - n
    - expand
    - rollout
    - backpropagate
    - is_fully_expanded
    - best_child

"""

import copy
from collections import defaultdict
from pygame.locals import *
import pygame
import sys
import random
import config
import stats
import numpy as np


class Player:
    def __init__(self, token_color, board, difficulty, algorithm=None):
        self.token_color = token_color
        self.board = board
        self.difficulty = difficulty
        self.algorithm = algorithm if algorithm is not None else '_'  # in case of Human, it never uses algorithm so
        # its irrelevant to pass
        self.ai_player = None

    def wait_a_second(self, game, initial_token_coord):
        pygame.time.wait(1000)
        pygame.draw.circle(
            game.WINDOW_SURF,
            config.GREEN,
            game.translate_grid_to_pixel_coord(initial_token_coord, self.board),
            int(self.board.GRID_SIZE * 0.5),
            10)

        game.main_clock.tick(config.FPS)
        pygame.display.update()
        game.main_clock.tick(config.FPS)

        pygame.time.wait(1000)

    def evaluate_current_state(self, grid):
        # CALCULATES AI VS HUMAN SCORE ACCORDING TO THEIR:
        #    NUMBER OF PIECES
        #    WEAK/STRONG INTERSECTION POINTS
        # and returns a % value of + or - . The more + the higher the chance of winning for AI
        # print("when evalation function called, AI_state cutoff\n")
        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        # special grid coordinates that have position advantage - Strong intersections
        # for all sizes
        for (column, row) in [(1, 1)]:
            if grid[column][row]['token_color'] == self.token_color:
                ai_token_remain += 0.5
            elif grid[column][row]['token_color'] is not config.EMPTY:
                human_token_remain -= 0.5

        # for 5x5 and 9x5
        if self.board.GRID_COLS >= 5:
            for (column, row) in [(1, 3), (3, 1), (3, 3)]:
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        # for 9x5
        if self.board.GRID_COLS == 9:
            for (column, row) in [(5, 1), (5, 3), (7, 1), (7, 3)]:
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        return (ai_token_remain - human_token_remain) * 1.0 / (ai_token_remain + human_token_remain)

    def terminal_test(self, grid):
        # print(("terminal_test is called, the current state is: \n", 'AI_state', '\n'))

        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        # print(("within terminaltest\n ", ai_token_remain, human_token_remain, '\n'))

        if ai_token_remain == 0 or human_token_remain == 0:
            return True
        else:
            return False

    def utility(self, grid):
        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        if ai_token_remain == 0:
            # print("AI left nothing\n")
            return -1
        elif human_token_remain == 0:
            # print("human left nothing")
            return 1

    def check_movable_token_table(self, token_color, grid, game):
        movable_token_table: dict = self.board.get_movable_token_information(token_color, grid)
        return movable_token_table


class Human(Player):

    def check_if_hint_clicked(self, game, mouse_x, mouse_y):
        hint_button_clicked = game.hint_button_rect.collidepoint(mouse_x - game.button_hx, mouse_y - game.button_hy)
        if hint_button_clicked:
            return True

    def make_turn(self, grid, game):
        human_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)

        if human_movable_token_table != {}:
            hint = MinimaxAlphaBeta(self.token_color, self.board, 2, self.algorithm)
            calc_hint = hint.give_hint(grid, game)

        if self.terminal_test(grid):
            return None

        initial_token_coord = None
        final_token_coord = None
        show_hint = False
        while final_token_coord is None:
            if show_hint:
                game.draw_hint(calc_hint)
            while initial_token_coord is None:
                if show_hint:
                    game.draw_hint(calc_hint)
                for event in pygame.event.get():
                    game.main_clock.tick(config.FPS)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        initial_token_coord = game.get_grid_clicked((mouse_x, mouse_y), self.board)
                        if self.check_if_hint_clicked(game, mouse_x, mouse_y):
                            show_hint = True
                        elif initial_token_coord not in human_movable_token_table:
                            initial_token_coord = None

                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            # when grid got clicked, extra green circle shows it
            pygame.draw.circle(
                game.WINDOW_SURF,
                config.GREEN,
                game.translate_grid_to_pixel_coord(initial_token_coord, self.board),
                int(self.board.GRID_SIZE * 0.5),
                10)

            game.main_clock.tick(config.FPS)
            pygame.display.update()
            game.main_clock.tick(config.FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    final_token_coord = game.get_grid_clicked((mouse_x, mouse_y), self.board)
                    # to detect if the user changes the token he wants to move
                    if final_token_coord not in human_movable_token_table[initial_token_coord]:
                        if final_token_coord in human_movable_token_table:
                            initial_token_coord = final_token_coord
                            final_token_coord = None

                            game.draw_grid(grid, self.board)
                            pygame.draw.circle(
                                game.WINDOW_SURF,
                                config.GREEN,
                                game.translate_grid_to_pixel_coord(initial_token_coord, self.board),
                                int(self.board.GRID_SIZE * 0.5),
                                10)

                            game.main_clock.tick(config.FPS)
                            pygame.display.update()
                            game.main_clock.tick(config.FPS)
                        else:
                            final_token_coord = None

        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board, True)
        return new_grid


class AI(Player):

    def __init__(self, token_color, board, difficulty, algorithm):
        super().__init__(token_color, board, difficulty, algorithm)
        self.total_node_generated = 0
        self.depth_of_game_tree = 0
        self.is_cutoff = False

    def initialize_ai_player(self):
        if self.difficulty == 'Easy':
            self.ai_player = Random(self.token_color, self.board, self.difficulty, self.algorithm)

        elif self.difficulty == 'Medium' and self.algorithm == 'Minimax' and self.board.GRID_COLS < 9:
            self.ai_player = Minimax(self.token_color, self.board, 3, self.algorithm)
        elif self.difficulty == 'Medium' and self.algorithm == 'Minimax' and self.board.GRID_COLS == 9:
            self.ai_player = Minimax(self.token_color, self.board, 2, self.algorithm)

        elif self.difficulty == 'Medium' and self.algorithm == 'Minimax_AlphaBeta' and self.board.GRID_COLS < 9:
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 3, self.algorithm)
        elif self.difficulty == 'Medium' and self.algorithm == 'Minimax_AlphaBeta' and self.board.GRID_COLS == 9:
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 2, self.algorithm)

        elif self.difficulty == 'Medium' and self.algorithm == 'Monte_Carlo_TS' and self.board.GRID_COLS < 9:
            self.ai_player = MonteCarloTS(self.token_color, self.board, (float('inf'), 100), self.algorithm)
        elif self.difficulty == 'Medium' and self.algorithm == 'Monte_Carlo_TS' and self.board.GRID_COLS == 9:
            self.ai_player = MonteCarloTS(self.token_color, self.board, (500, 10), self.algorithm, )

        elif self.difficulty == 'Hard' and self.algorithm == 'Minimax' and self.board.GRID_COLS < 9:
            self.ai_player = Minimax(self.token_color, self.board, 5, self.algorithm)
        elif self.difficulty == 'Hard' and self.algorithm == 'Minimax' and self.board.GRID_COLS == 9:
            self.ai_player = Minimax(self.token_color, self.board, 4, self.algorithm)

        elif self.difficulty == 'Hard' and self.algorithm == 'Minimax_AlphaBeta' and self.board.GRID_COLS < 9:
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 5, self.algorithm)
        elif self.difficulty == 'Hard' and self.algorithm == 'Minimax_AlphaBeta' and self.board.GRID_COLS == 9:
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 4, self.algorithm)

        elif self.difficulty == 'Hard' and self.algorithm == 'Monte_Carlo_TS' and self.board.GRID_COLS < 9:
            self.ai_player = MonteCarloTS(self.token_color, self.board, (float('inf'), 500), self.algorithm)
        elif self.difficulty == 'Hard' and self.algorithm == 'Monte_Carlo_TS' and self.board.GRID_COLS == 9:
            self.ai_player = MonteCarloTS(self.token_color, self.board, (500, 20), self.algorithm)

    def make_turn(self, grid, game):
        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        if ai_movable_token_table != {}:
            return self.ai_player.play(ai_movable_token_table, game, grid)
        else:
            return False

    def evaluate_current_state_a(self, grid):
        # CALCULATES AI VS HUMAN SCORE ACCORDING TO THEIR:
        #    NUMBER OF PIECES
        #    WEAK/STRONG INTERSECTION POINTS
        # and returns a % value of + or - . The more + the higher the chance of winning for AI
        # print("when evalation function called, AI_state cutoff\n")
        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        # special grid coordinates that have position advantage - Strong intersections
        # for all sizes
        for (column, row) in [(1, 1)]:
            if grid[column][row]['token_color'] == self.token_color:
                ai_token_remain += 0.5
            elif grid[column][row]['token_color'] is not config.EMPTY:
                human_token_remain -= 0.5

        # for 5x5 and 9x5
        if self.board.GRID_COLS >= 5:
            for (column, row) in [(1, 3), (3, 1), (3, 3)]:
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        # for 9x5
        if self.board.GRID_COLS == 9:
            for (column, row) in [(5, 1), (5, 3), (7, 1), (7, 3)]:
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        return (ai_token_remain - human_token_remain) * 1.0 / (ai_token_remain + human_token_remain)

    def evaluate_current_state_b(self, grid, token, bias=True):  # TODO - is we have time
        # CALCULATES AI VS HUMAN SCORE ACCORDING TO THEIR:
        #    NUMBER OF PIECES
        #    WEAK/STRONG INTERSECTION POINTS
        # and returns a % value of + or - . The more + the higher the chance of winning for AI
        # print("when evalation function called, AI_state cutoff\n")
        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == token:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        # special grid coordinates that have position advantage - Strong intersections
        # for all sizes
        for (column, row) in [(1, 1)]:
            if grid[column][row]['token_color'] == token:
                ai_token_remain += 0.5
            elif grid[column][row]['token_color'] is not config.EMPTY:
                human_token_remain -= 0.5

        # for 5x5 and 9x5
        if self.board.GRID_COLS >= 5:
            for (column, row) in [(1, 3), (3, 1), (3, 3)]:
                if grid[column][row]['token_color'] == token:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        # for 9x5
        if self.board.GRID_COLS == 9:
            for (column, row) in [(5, 1), (5, 3), (7, 1), (7, 3)]:
                if grid[column][row]['token_color'] == token:
                    ai_token_remain += 0.5
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain -= 0.5

        ai_score = (ai_token_remain - human_token_remain) * 1.0 / (ai_token_remain + human_token_remain)
        human_score = (human_token_remain - ai_token_remain) * 1.0 / (ai_token_remain + human_token_remain)

        print("Current scores: ", ai_score, human_score)
        if bias:
            return [ai_score, human_score]
        if ai_token_remain == 0:
            return [0, 1]
        elif human_token_remain == 0:
            return [1, 0]
        else:
            return [0.5, 0.5]

    def terminal_test(self, grid):
        # print(("terminal_test is called, the current state is: \n", 'AI_state', '\n'))

        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        # print(("within terminaltest\n ", ai_token_remain, human_token_remain, '\n'))

        if ai_token_remain == 0 or human_token_remain == 0:
            return True
        else:
            return False

    def utility(self, grid):
        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        if ai_token_remain == 0:
            # print("AI left nothing\n")
            return -1
        elif human_token_remain == 0:
            # print("human left nothing")
            return 1


class Random(AI):
    def play(self, ai_movable_token_table, game, grid):
        if self.terminal_test(grid):
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()

        initial_token_coord = list(ai_movable_token_table.keys())[0]
        final_token_coord = list(ai_movable_token_table[initial_token_coord].keys())[0]

        self.wait_a_second(game, initial_token_coord)

        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid


class Minimax(AI):

    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord, final_token_coord = self.minimax_search(grid, game)
        self.wait_a_second(game, initial_token_coord)
        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid

    def minimax_search(self, grid, game):
        ai_current_action = {}
        v = self.max_value(grid, game, 0, ai_current_action)
        return ai_current_action[v]

    def max_value(self, grid, game, depth, ai_current_action):
        self.total_node_generated += 1

        if depth >= self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_v = float('-inf')

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state_a(grid)

        if self.terminal_test(grid):
            return self.utility(grid)

        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):

                current_AI_state = copy.deepcopy(grid)
                result_grid = game.make_move(self.token_color, current_AI_state, start_grid_coord, end_grid_coord,
                                             self.board)

                v = self.min_value(result_grid, game, depth + 1, ai_current_action)
                if v > current_v:
                    current_v = v
                    if depth == 0:
                        ai_current_action[current_v] = (start_grid_coord, end_grid_coord)

        return current_v

    def min_value(self, grid, game, depth, ai_current_action):
        self.total_node_generated += 1

        if depth > self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state_a(grid)

        if self.terminal_test(grid):
            return self.utility(grid)

        if self.token_color == config.WHITE:
            human_token = config.BLACK
        else:
            human_token = config.WHITE

        ai_movable_token_table = self.check_movable_token_table(human_token, grid, game)

        current_v = float('inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):

                current_human_state = copy.deepcopy(grid)

                new_grid = game.make_move(human_token, current_human_state, start_grid_coord, end_grid_coord,
                                          self.board)

                v = self.max_value(new_grid, game, depth + 1, ai_current_action)
                if v < current_v:
                    current_v = v

        return current_v


class MinimaxAlphaBeta(AI):

    def __init__(self, token_color, board, difficulty, algorithm):
        super().__init__(token_color, board, difficulty, algorithm)
        self.pruning_in_max_value = 0
        self.pruning_in_min_value = 0

    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord, final_token_coord = self.alpha_beta_search(grid, game)
        self.wait_a_second(game, initial_token_coord)
        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid

    def give_hint(self, grid, game):
        initial_token_coord, final_token_coord = self.alpha_beta_search(grid, game)
        return [initial_token_coord, final_token_coord]

    def alpha_beta_search(self, grid, game, alpha=-1, beta=1):
        ai_current_action = {}
        v = self.max_value(grid, game, alpha, beta, 0, ai_current_action)
        return ai_current_action[v]

    def max_value(self, grid, game, alpha, beta, depth, ai_current_action):
        # print(("\nin max_value body, called ", depth, " levels, current state:\n ", 'AI_state', '\n'))

        self.total_node_generated += 1

        if depth >= self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_alpha = alpha
        current_beta = beta

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state_a(grid)

        if self.terminal_test(grid):
            # print("return since max_value terminated ")
            return self.utility(grid)

        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        current_v = float('-inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                # print(("in max_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

                current_AI_state = copy.deepcopy(grid)
                result_grid = game.make_move(self.token_color, current_AI_state, start_grid_coord, end_grid_coord,
                                             self.board)

                v = self.min_value(result_grid, game, current_alpha, current_beta, depth + 1, ai_current_action)
                if v > current_v:
                    current_v = v
                    if depth == 0:
                        ai_current_action[current_v] = (start_grid_coord, end_grid_coord)

                    if current_v >= beta:
                        self.pruning_in_max_value += 1
                        # print(("return since max_value pruning: ", current_v))
                        return current_v
                    current_alpha = max(alpha, current_v)
        # print(("return since all level done in max_value: ", current_v))
        return current_v

    def min_value(self, grid, game, alpha, beta, depth, ai_current_action):
        # print(("in min_value body, called ", depth, " level, current state:\n\n ", 'AI_state', '\n\n'))

        self.total_node_generated += 1

        if depth > self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_alpha = alpha
        current_beta = beta

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state_a(grid)

        if self.terminal_test(grid):
            # print("return since terminated")
            return self.utility(grid)
        if self.token_color == config.WHITE:
            human_token = config.BLACK
        else:
            human_token = config.WHITE

        ai_movable_token_table = self.check_movable_token_table(human_token, grid, game)

        current_v = float('inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                # print(("in min_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

                current_human_state = copy.deepcopy(grid)

                new_grid = game.make_move(human_token, current_human_state, start_grid_coord, end_grid_coord,
                                          self.board)

                v = self.max_value(new_grid, game, current_alpha, current_beta, depth + 1, ai_current_action)
                if v < current_v:

                    current_v = v

                    if current_v <= alpha:
                        self.pruning_in_min_value += 1
                        # print(("return since min_value pruning: ", current_v))
                        return current_v
                    current_beta = min(beta, current_v)

        # print(("return since all level done in min_value: ", current_v))
        return current_v


class MonteCarloTS(AI):

    def __init__(self, token_color, board, difficulty, algorithm):
        super().__init__(token_color, board, difficulty, algorithm)
        self.root = None

    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord, final_token_coord = self.mct_search(grid, game, self.difficulty[0], self.difficulty[1])
        self.wait_a_second(game, initial_token_coord)
        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid

    def mct_search(self, grid, game, max_rollout_depth=500, n_iterations=20, epsilon=2):
        self.root = Node(grid, game, self.token_color, self.board, self.difficulty, self.algorithm)
        for _ in range(n_iterations):
            self.run_iteration(max_rollout_depth)
            # to select best child go for exploitation only
        best_child = self.root.best_child(epsilon=epsilon)
        action, node = best_child.parent
        print(action, node.results)
        return action

    def run_iteration(self, max_rollout_depth):
        v = self.tree_policy()
        reward = v.rollout(max_depth=max_rollout_depth)
        v.backpropagate(reward)
        print("Reward: ", reward)

    def tree_policy(self):
        current_node = self.root
        while not self.terminal_test(current_node.grid):
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node


class Node(AI):

    def __init__(self, grid, game, token_color, board, difficulty, algorithm, parent=(None, None)):
        super().__init__(token_color, board, difficulty, algorithm)
        self.token = "White" if token_color == config.WHITE else "Black"
        self.token_inv = "Black" if token_color == config.WHITE else "White"
        self.grid = copy.deepcopy(grid)
        self.game = game
        self.parent = parent  # tuppple: (action, node object); action = [(initial coord),(final_coord)]
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(lambda: 0)  # wins and losses for each node
        self.untried_actions = self.get_untried_actions(self.grid, self.token_color)

    def get_untried_actions(self, grid, token_color):
        movable_dict = self.check_movable_token_table(token_color, grid, game=None)
        keys = list(movable_dict.keys())
        moves = []
        for k in keys:
            for m in movable_dict[k]:
                moves.append([k, m])
        return moves

    def q(self):
        wins = self.results[self.token]
        loses = self.results[self.token_inv]
        return wins - loses

    def n(self):
        return self.number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = copy.deepcopy(self.grid)
        result_grid = self.game.make_move(self.token_color, next_state, action[0], action[1], self.board)
        new_token = config.WHITE if self.token_color == config.BLACK else config.BLACK
        child_node = Node(result_grid, self.game, new_token, self.board, self.difficulty, self.algorithm,
                          parent=(action, self))
        self.children.append(child_node)
        return child_node

    def rollout(self, max_depth):
        current_state = copy.deepcopy(self.grid)
        current_player = self.token_color
        depth = max_depth
        # starts from current grid and goes through possible moves if the game simulation is not over
        while depth and not self.terminal_test(current_state):
            possible_moves = self.get_untried_actions(current_state, current_player)
            scores = []
            # for each possible move calculate the score
            for move in possible_moves:
                state = copy.deepcopy(current_state)
                result_grid = self.game.make_move(current_player, state, move[0], move[1], self.board)
                # get current score to choose next move in simulation
                score = self.evaluate_current_state_b(result_grid, current_player)
                scores.append(score[0])

            # which next move has higher score
            idx = np.argmax(scores)
            max_move = possible_moves[idx]

            # make the move and update grid
            current_state = self.game.make_move(current_player, current_state, max_move[0], max_move[1], self.board)
            # Change turn of player in simulation
            current_player = config.WHITE if current_player == config.BLACK else config.BLACK
            depth -= 1

        # game simulation is over and calulate win and loss
        win_loss = self.evaluate_current_state_b(current_state, current_player, bias=False)
        win_loss_d = {}
        current_token = "White" if current_player == config.WHITE else "Black"
        current_token_inv = "Black" if current_player == config.WHITE else "White"
        win_loss_d[current_token_inv] = win_loss[0]
        win_loss_d[current_token] = win_loss[1]
        return win_loss_d

    def backpropagate(self, win_loss):
        self.number_of_visits += 1.
        self.results[self.token] += win_loss[self.token]  # value backed up.
        self.results[self.token_inv] += win_loss[self.token_inv]
        _, parent = self.parent
        # propagates wins and losses up the tree to the root
        if parent:
            parent.backpropagate(win_loss)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, epsilon=2):
        choices_weights = [(c.q() / c.n()) + epsilon * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]
