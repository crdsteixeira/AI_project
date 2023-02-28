'''
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

Player.py:

Functions:

- make_turn: Human
- make_turn: AI
- is_within_grid: TODO -- XX its in Board.py

# MINIMAX:
- max_value
- min_value
- alpha_beta_search
- terminal_test
- utility
- evaluate_current_state

'''

import copy

from pygame.locals import *
import pygame
import sys
import random
import config


class Player:
    def __init__(self, token_color, board, difficulty, algorithm):
        self.token_color = token_color
        self.board = board
        self.difficulty = difficulty
        self.algorithm = algorithm
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

    def check_movable_token_table(self, token_color, grid, game):
        movable_token_table: dict = self.board.get_movable_token_information(token_color, grid)
        if movable_token_table == {}:
            game.show_game_results()
        game.check_for_draw()  # TODO

        return movable_token_table


class Human(Player):
    def make_turn(self, grid, game):

        human_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)

        initial_token_coord = None
        final_token_coord = None
        while final_token_coord is None:
            while initial_token_coord is None:
                for event in pygame.event.get():
                    game.main_clock.tick(config.FPS)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        initial_token_coord = game.get_grid_clicked((mouse_x, mouse_y), self.board)
                        if initial_token_coord not in human_movable_token_table:
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
        self.pruning_in_max_value = 0
        self.pruning_in_min_value = 0
        self.depth_of_game_tree = 0
        self.is_cutoff = False

    def initialize_ai_player(self):
        if self.difficulty == 'Easy':
            self.ai_player = Random(self.token_color, self.board, self.difficulty, self.algorithm)
        elif self.difficulty == 'Medium' and self.algorithm == 'Minimax_AlphaBeta':
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 3, self.algorithm)
        elif self.difficulty == 'Medium' and self.algorithm == 'Monte_Carlo_TS':
            pass
        elif self.difficulty == 'Hard' and self.algorithm == 'Minimax_AlphaBeta':
            self.ai_player = MinimaxAlphaBeta(self.token_color, self.board, 7, self.algorithm)
        elif self.difficulty == 'Hard' and self.algorithm == 'Monte_Carlo_TS':
            pass

    def make_turn(self, grid, game):
        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        return self.ai_player.play(ai_movable_token_table, game, grid)
    
    
    def evaluate_current_state(self, grid):
    # CALCULATES AI VS HUMAN SCORE ACCORDING TO THEIR:
    #    NUMBER OF PIECES
    #    WEAK/STRONG INTERSECTION POINTS
    # and returns a % value of + or - . The more + the higher the chance of winning for AI
        print("when evalation function called, AI_state cutoff\n")
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
        pass

    def terminal_test(self, grid):
        print(("terminal_test is called, the current state is: \n", 'AI_state', '\n'))

        ai_token_remain = 0
        human_token_remain = 0

        for column in range(self.board.GRID_COLS):
            for row in range(self.board.GRID_ROWS):
                if grid[column][row]['token_color'] == self.token_color:
                    ai_token_remain += 1
                elif grid[column][row]['token_color'] is not config.EMPTY:
                    human_token_remain += 1

        print(("within terminaltest\n ", ai_token_remain, human_token_remain, '\n'))

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
            print("AI left nothing\n")
            return -1
        elif human_token_remain == 0:
            print("human left nothing")
            return 1


class Random(AI):
    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord = list(ai_movable_token_table.keys())[0]
        final_token_coord = list(ai_movable_token_table[initial_token_coord].keys())[0]

        self.wait_a_second(game, initial_token_coord)

        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid


class MinimaxAlphaBeta(AI):

    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord, final_token_coord = self.alpha_beta_search(grid, game)
        self.wait_a_second(game, initial_token_coord)
        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid

    def alpha_beta_search(self, grid, game, alpha=-1, beta=1):
        ai_current_action = {}
        v = self.max_value(grid, game, alpha, beta, 0, ai_current_action)
        return ai_current_action[v]

    def max_value(self, grid, game, alpha, beta, depth, ai_current_action):
        print(("\nin max_value body, called ", depth, " levels, current state:\n ", 'AI_state', '\n'))

        self.total_node_generated += 1

        if depth >= self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_alpha = alpha
        current_beta = beta

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state(grid)
        
        if self.terminal_test(grid):
            print("return since max_value terminated ")
            return self.utility(grid)

        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        current_v = float('-inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                print(("in max_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

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
                        print(("return since max_value pruning: ", current_v))
                        return current_v
                    current_alpha = max(alpha, current_v)
        print(("return since all level done in max_value: ", current_v))
        return current_v

    def min_value(self, grid, game, alpha, beta, depth, ai_current_action):
        print(("in min_value body, called ", depth, " level, current state:\n\n ", 'AI_state', '\n\n'))

        self.total_node_generated += 1

        if depth > self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_alpha = alpha
        current_beta = beta

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state(grid)
        
        if self.terminal_test(grid):
            print("return since terminated")
            return self.utility(grid)
        if self.token_color == config.WHITE:
            human_token = config.BLACK
        else:
            human_token = config.WHITE

        ai_movable_token_table = self.check_movable_token_table(human_token, grid, game)

        current_v = float('inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                print(("in min_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

                current_human_state = copy.deepcopy(grid)

                new_grid = game.make_move(human_token, current_human_state, start_grid_coord, end_grid_coord,
                                          self.board)

                v = self.max_value(new_grid, game, current_alpha, current_beta, depth + 1, ai_current_action)
                if v < current_v:

                    current_v = v

                    if current_v <= alpha:
                        self.pruning_in_min_value += 1
                        print(("return since min_value pruning: ", current_v))
                        return current_v
                    current_beta = min(beta, current_v)

        print(("return since all level done in min_value: ", current_v))
        return current_v


class Minimax(AI):

    def play(self, ai_movable_token_table, game, grid):
        initial_token_coord, final_token_coord = self.minimax_search(grid, game)
        self.wait_a_second(game, initial_token_coord)
        new_grid = game.make_move(self.token_color, grid, initial_token_coord, final_token_coord, self.board,
                                  False)
        return new_grid

    def minimax_search(self, grid, game, alpha=-1, beta=1):
        ai_current_action = {}
        v = self.max_value(grid, game, 0, ai_current_action)
        return ai_current_action[v]

    def max_value(self, grid, game, depth, ai_current_action):
        print(("\nin max_value body, called ", depth, " levels, current state:\n ", 'AI_state', '\n'))

        self.total_node_generated += 1

        if depth >= self.depth_of_game_tree:
            self.depth_of_game_tree = depth

        current_v = float('-inf')

        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state(grid)
        
        if self.terminal_test(grid):
            print("return since max_value terminated ")
            return self.utility(grid)

        ai_movable_token_table = self.check_movable_token_table(self.token_color, grid, game)
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                print(("in max_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

                current_AI_state = copy.deepcopy(grid)
                result_grid = game.make_move(self.token_color, current_AI_state, start_grid_coord, end_grid_coord,
                                             self.board)

                v = self.min_value(result_grid, game, depth + 1, ai_current_action)
                if v > current_v:
                    current_v = v
                    if depth == 0:
                        ai_current_action[current_v] = (start_grid_coord, end_grid_coord)


        print(("return since all level done in max_value: ", current_v))
        return current_v

    def min_value(self, grid, game, depth, ai_current_action):
        print(("in min_value body, called ", depth, " level, current state:\n\n ", 'AI_state', '\n\n'))

        self.total_node_generated += 1

        if depth > self.depth_of_game_tree:
            self.depth_of_game_tree = depth


        if depth >= int(self.difficulty):  # cutoff setting, maximum level AI can search through
            self.is_cutoff = True
            return self.evaluate_current_state(grid)
        
        if self.terminal_test(grid):
            print("return since terminated")
            return self.utility(grid)
        
        if self.token_color == config.WHITE:
            human_token = config.BLACK
        else:
            human_token = config.WHITE

        ai_movable_token_table = self.check_movable_token_table(human_token, grid, game)

        current_v = float('inf')
        for start_grid_coord in list(ai_movable_token_table.keys()):
            for end_grid_coord in list(ai_movable_token_table[start_grid_coord].keys()):
                print(("in min_value body, action is choose from ", start_grid_coord, end_grid_coord, '\n\n'))

                current_human_state = copy.deepcopy(grid)

                new_grid = game.make_move(human_token, current_human_state, start_grid_coord, end_grid_coord,
                                          self.board)

                v = self.max_value(new_grid, game, depth + 1, ai_current_action)
                if v < current_v:
                    current_v = v

        print(("return since all level done in min_value: ", current_v))
        return current_v

        