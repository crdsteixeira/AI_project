'''
AI - MECD - FEUP
February 2023
Rojan Aslani, Catia Teixeira

Game.py:

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
- show_game_results: TODO -- its in main - because of the floating window I couldnt pass the floating window through a function
- check for draw: TODO
'''

import pygame
import sys
import config


class Game:
    def __init__(self, WINDOW_SURF, main_clock, FONT):
        self.titles = {
            'player_1': {'Choose player 1 (White tokens)': ["Human", "Minimax", "Minimax_AlphaBeta", "Monte_Carlo_TS"]},
            'player_2': {'Choose player 2 (Black tokens)': ["Human", "Minimax", "Minimax_AlphaBeta", "Monte_Carlo_TS"]},
            'size': {'In which board size would you like to play with?': ["Fanoron-Telo (3 X 3)", "Fanoron-Dimy (5 X 5)", "Fanoron-Tsivy(9 X 5)"]},
            'difficulty': {'What is your difficulty level?': ["Easy", "Medium", "Hard"]}
        }
        self.WINDOW_SURF = WINDOW_SURF
        self.main_clock = main_clock
        self.FONT = FONT
        self.button_width = 110
        self.button_height = 30
        self.button_x = config.WINDOW_WIDTH - self.button_width - 10
        self.button_y = config.WINDOW_HEIGHT - self.button_height - 10
        self.selected_options = {}


    def draw_option(self, key, title, options, y):
        # Choose game mode
        text = self.FONT.render(title, True, config.BLACK)
        rect = text.get_rect()
        rect.center = (int(config.WINDOW_WIDTH * 0.5), int(config.WINDOW_HEIGHT * y))

        text_list = []
        delta_x = 1. / (len(options) + 1)
        x = delta_x
        text_list.append((key, text, rect, title, False, False))
        for opt in options:
            surf = self.FONT.render(opt, True, config.BLACK)
            rect = surf.get_rect()
            rect.center = (int(config.WINDOW_WIDTH * x), int(config.WINDOW_HEIGHT * (y + 0.05)))
            selected = self.selected_options.get(key, None) == opt
            text_list.append((key, surf, rect, opt, selected, True))
            x += delta_x

        return text_list

    def draw_all_options(self):
        y = 0.1
        delta_y = (1 / (len(self.titles)+1))
        text_list = []
        for key, value in self.titles.items():
            for title, options in value.items():
                text_list.append(self.draw_option(key, title, options, y))
                y += delta_y

        return text_list

    def draw_readytostart(self):
        # create the button surface and text
        button_surface = pygame.Surface((self.button_width, self.button_height))
        button_text = pygame.font.Font(None, 22).render("Ready to start", False, (255, 255, 255))

        # fill the button surface with a color
        button_surface.fill((0, 128, 0))

        return button_surface, button_text

    def draw_initial_screen(self):
        """Draws the text and handles the mouse click events for letting
        the player choose which color they want to be.
        Returns [WHITE_TOKEN, BLACK_TOKEN] if the player chooses to be White,
        [BLACK_TOKEN, WHITE_TOKEN] if Black.
        """
        text_list = self.draw_all_options()
        button_surface, button_text = self.draw_readytostart()

        while True:  # keep looping until the player has clicked on a color

            self.main_clock.tick(config.FPS)  # CPU is too fast that slowing down is needed
            self.WINDOW_SURF.fill(config.WHITE)
            # blit the button text onto the button surface
            button_rect = button_text.get_rect(center=(self.button_width / 2, self.button_height / 2))
            button_surface.blit(button_text, button_rect)

            # blit the button surface onto the game surface
            self.WINDOW_SURF.blit(button_surface, (self.button_x, self.button_y))

            for opt in text_list:
                for i, (key, surf, rect, text, selected, selectable) in enumerate(opt):
                    color = config.GREEN if selected else config.BLACK  # change text color based on selection status
                    if selectable:
                        new_surf = self.FONT.render(text, True, color)
                        self.WINDOW_SURF.blit(new_surf, rect)
                        opt[i] = (
                            key, new_surf, rect, text, selected, selectable)  # update the text_list to reflect changes
                    else:
                        self.WINDOW_SURF.blit(surf, rect)
            for event in pygame.event.get():  # event handling loop
                self.main_clock.tick(config.FPS)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # print 'click'
                    mouse_x, mouse_y = event.pos
                    for opt in text_list:
                        for i, (key, surf, rect, text, selected, selectable) in enumerate(opt):
                            if rect.collidepoint((mouse_x, mouse_y)) and selectable:
                                self.selected_options[opt[0][0]] = opt[i][3]  # update selected option
                                for j, (k, s, r, t, sel, sela) in enumerate(opt):
                                    opt[j] = (k, s, r, t, t == opt[i][3], True)  # update other options

                    button_clicked = button_rect.collidepoint(mouse_x - self.button_x, mouse_y - self.button_y)
                    if button_clicked:
                        pygame.event.clear()
                        return self.selected_options

            self.main_clock.tick(config.FPS)
            pygame.display.update()
            self.main_clock.tick(config.FPS)

    def draw_circle(self, board, coords, text, color):  # print coords on board
        pcolor = pygame.Color(color)
        text_f = self.FONT.render(text, True, pygame.Color(255, 255, 255) - pcolor)
        pygame.draw.circle(self.WINDOW_SURF, color, coords, int(board.GRID_SIZE * 0.5))
        self.WINDOW_SURF.blit(text_f, text_f.get_rect(center=coords))

    def draw_grid(self, grid, board):
        if board.GRID_COLS == 3:
            bg_image = pygame.image.load('./images/ThreeByThree.png')
        if board.GRID_COLS == 5:
            bg_image = pygame.image.load('./images/FiveByFive.png')
        if board.GRID_COLS == 9:
            bg_image = pygame.image.load('./images/NineByFive.png')

        bg_image = pygame.transform.smoothscale(bg_image,
                                                (int(config.WINDOW_WIDTH * 0.5), int(config.WINDOW_HEIGHT * 0.5)))
        self.WINDOW_SURF.fill(config.WHITE)
        self.WINDOW_SURF.blit(
            bg_image,
            (int(config.WINDOW_WIDTH * 0.25), int(config.WINDOW_HEIGHT * 0.25)))

        for column in range(board.GRID_COLS):
            for row in range(board.GRID_ROWS):
                center_pixel_coord = self.translate_grid_to_pixel_coord((column, row), board)
                # draw token with outline
                if grid[column][row]['token_color'] != config.EMPTY:
                    # print coords on board
                    self.draw_circle(board, center_pixel_coord, "{0}, {1}".format(column, row),
                                     grid[column][row]['token_color'])
                    #pygame.draw.circle(
                    #    self.WINDOW_SURF,
                    #    grid[column][row]['token_color'],
                    ##    center_pixel_coord,
                    #   int(board.GRID_SIZE * 0.5))

                    pygame.draw.circle(
                        self.WINDOW_SURF,
                        config.BLACK,
                        center_pixel_coord,
                        int(board.GRID_SIZE * 0.5),
                        2)
                else:
                    # print coords on board
                    self.draw_circle(board, center_pixel_coord, "{0}, {1}".format(column, row),
                                     config.GRAY)

        self.main_clock.tick(config.FPS)
        pygame.display.update()
        self.main_clock.tick(config.FPS)

    def translate_grid_to_pixel_coord(self, coords, board):
        (grid_column, grid_row) = coords
        if board.GRID_COLS == 3:
            x = grid_column * int(config.WINDOW_HEIGHT * 0.25) + int(config.WINDOW_HEIGHT * 0.25), \
                grid_row * int(config.WINDOW_WIDTH * 0.25) + int(config.WINDOW_WIDTH * 0.25)
        if board.GRID_COLS == 5:
            x = grid_column * int(config.WINDOW_HEIGHT * 0.125) + int(config.WINDOW_HEIGHT * 0.25), \
                grid_row * int(config.WINDOW_WIDTH * 0.125) + int(config.WINDOW_WIDTH * 0.25)

        if board.GRID_COLS == 9:
            x = grid_column * int(config.WINDOW_HEIGHT * 0.0625) + int(config.WINDOW_HEIGHT * 0.25), \
                grid_row * int(config.WINDOW_WIDTH * 0.125) + int(config.WINDOW_WIDTH * 0.25)
        return x

    def get_grid_clicked(self, coords, board):
        """ Return a tuple of two integers of the grid space coordinates where
        the mouse was clicked. (Or returns None not in any space.)
        """
        (mouse_x, mouse_y) = coords
        for column in range(board.GRID_COLS):
            for row in range(board.GRID_ROWS):
                (center_x, center_y) = self.translate_grid_to_pixel_coord((column, row), board)
                if (center_x - int(board.GRID_SIZE * 0.5) < mouse_x < center_x + int(board.GRID_SIZE * 0.5) and
                        center_y - int(board.GRID_SIZE * 0.5) < mouse_y < center_y + int(board.GRID_SIZE * 0.5)):
                    print(column, row)
                    return column, row
        return None

    def make_move(self, token_color, grid, initial_token_coords, final_token_coords, board, prompt_bi_direct=False):
        (click_x, click_y) = initial_token_coords
        (move_x, move_y) = final_token_coords
        movable_token_table = board.get_movable_token_information(token_color, grid, prompt_bi_direct)

        grid[click_x][click_y]['token_color'] = config.EMPTY
        grid[move_x][move_y]['token_color'] = token_color

        if prompt_bi_direct and movable_token_table[(click_x, click_y)][(move_x, move_y)] == 'bi-direction':
            text_surf = self.FONT.render('Do you choose to approach or withdraw~?', True, config.BLACK)
            text_rect = text_surf.get_rect()
            text_rect.center = (int(config.WINDOW_WIDTH * 0.5), int(config.WINDOW_HEIGHT * 0.875))

            approach_surf = self.FONT.render('Approach', True, config.BLACK)
            approach_rect = approach_surf.get_rect()
            approach_rect.center = (int(config.WINDOW_WIDTH * 0.375), int(config.WINDOW_HEIGHT * 0.9375))

            withdraw_surf = self.FONT.render('Withdraw', True, config.BLACK)
            withdraw_rect = withdraw_surf.get_rect()
            withdraw_rect.center = (int(config.WINDOW_WIDTH * 0.625), int(config.WINDOW_HEIGHT * 0.9375))

            is_chosen = False
            while not is_chosen:  # prompt the Human player to choose between approach or withdraw capture
                self.main_clock.tick(config.FPS)
                for event in pygame.event.get():
                    self.main_clock.tick(config.FPS)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if approach_rect.collidepoint((mouse_x, mouse_y)):
                            movable_token_table[(click_x, click_y)][(move_x, move_y)] = 'approach'
                            is_chosen = True
                            break
                        elif withdraw_rect.collidepoint((mouse_x, mouse_y)):
                            movable_token_table[(click_x, click_y)][(move_x, move_y)] = 'withdraw'
                            is_chosen = True
                            break

                self.WINDOW_SURF.blit(text_surf, text_rect)
                self.WINDOW_SURF.blit(approach_surf, approach_rect)
                self.WINDOW_SURF.blit(withdraw_surf, withdraw_rect)
                self.main_clock.tick(config.FPS)
                pygame.display.update()
                self.main_clock.tick(config.FPS)

        delta_x, delta_y = (move_x - click_x, move_y - click_y)

        # there exist other opponent's token consecutively along on the same direction,
        # they also will be capture, in a 5X5 grid, maximally THREE in a roll.

        if movable_token_table[(click_x, click_y)][(move_x, move_y)] == 'approach':  # approach capture
            grid[click_x + 2 * delta_x][click_y + 2 * delta_y]['token_color'] = config.EMPTY

            if board.is_within_grid(click_x + 3 * delta_x, click_y + 3 * delta_y) and \
                    grid[click_x + 3 * delta_x][click_y + 3 * delta_y]['token_color'] != token_color and \
                    grid[click_x + 3 * delta_x][click_y + 3 * delta_y]['token_color'] != config.EMPTY:
                grid[click_x + 3 * delta_x][click_y + 3 * delta_y]['token_color'] = config.EMPTY

                if board.is_within_grid(click_x + 4 * delta_x, click_y + 4 * delta_y) and \
                        grid[click_x + 4 * delta_x][click_y + 4 * delta_y]['token_color'] != token_color and \
                        grid[click_x + 4 * delta_x][click_y + 4 * delta_y]['token_color'] != config.EMPTY:
                    grid[click_x + 4 * delta_x][click_y + 4 * delta_y]['token_color'] = config.EMPTY

        if movable_token_table[(click_x, click_y)][(move_x, move_y)] == 'withdraw':  # withdraw capture
            grid[click_x - delta_x][click_y - delta_y]['token_color'] = config.EMPTY

            if board.is_within_grid(click_x - 2 * delta_x, click_y - 2 * delta_y) and \
                    grid[click_x - 2 * delta_x][click_y - 2 * delta_y]['token_color'] != token_color and \
                    grid[click_x - 2 * delta_x][click_y - 2 * delta_y]['token_color'] != config.EMPTY:
                grid[click_x - 2 * delta_x][click_y - 2 * delta_y]['token_color'] = config.EMPTY

                if board.is_within_grid(click_x - 3 * delta_x, click_y - 3 * delta_y) and \
                        grid[click_x - 3 * delta_x][click_y - 3 * delta_y]['token_color'] != token_color and \
                        grid[click_x - 3 * delta_x][click_y - 3 * delta_y]['token_color'] != config.EMPTY:
                    grid[click_x - 3 * delta_x][click_y - 3 * delta_y]['token_color'] = config.EMPTY

        #print(("Make move from ", (click_x, click_y), ' to ', (move_x, move_y)))
        #print(('\n', '\n', '\n'))
        return grid


    def check_for_draw(self):
        pass

    # def check_for_draw(self, AI_state, turn):
    #     """check for draw in 3X3 grid by whether the state matches certain patterns
    #     """
    #     AI_token_remain_grid_coord = []
    #     human_token_remain_grid_coord = []
    #     AI_token_non_central_displacement = ()
    #     human_token_non_central_displacement = ()

    #     for column in range(self.board.GRID_COLS):
    #         for row in range(self.board.GRID_ROWS):
    #             if AI_state[column][row]['token_color'] == AI_token:
    #                 AI_token_remain_grid_coord.append((column, row))
    #             if AI_state[column][row]['token_color'] == human_token:
    #                 human_token_remain_grid_coord.append((column, row))

    #     # pattern 1
    #     if turn == 'AI' and AI_state[1][1]['token_color'] == AI_token and \
    #         len(AI_token_remain_grid_coord) == 2 and len(human_token_remain_grid_coord) == 1:
    #         for (column, row) in AI_token_remain_grid_coord:
    #             if column != 1 and row != 1:
    #                 AI_token_non_central_displacement = (column - 1, row - 1)
    #         for (column, row) in human_token_remain_grid_coord:
    #             human_token_non_central_displacement = (1 - column, 1 - row)

    #         if AI_token_non_central_displacement == human_token_non_central_displacement:
    #             show_game_results('', '', True)


    #     # pattern 2
    #     if turn == 'Human' and AI_state[1][1]['token_color'] == human_token and \
    #         len(AI_token_remain_grid_coord) == 1 and len(human_token_remain_grid_coord) == 2:
    #         for (column, row) in human_token_remain_grid_coord:
    #             if column != 1 and row != 1:
    #                 human_token_non_central_displacement = (column - 1, row - 1)
    #         for (column, row) in AI_token_remain_grid_coord:
    #             AI_token_non_central_displacement = (1 - column, 1 - row)

    #         if AI_token_non_central_displacement == human_token_non_central_displacement:
    #             show_game_results('', '', True)
                


    # def show_game_results(self):
    #     pass

    # def show_game_results(self, winner_str, BIG_FONT, draw=False):
    #     global total_node_generated
    #     global depth_of_game_tree
    #     print ("\n\nfinally,  level is, nodes are ", depth_of_game_tree, '\n\n', total_node_generated)
    #     if draw:
    #         text_surf = BIG_FONT.render('The game is draw', True, config.BLACK)
    #         text_rect = text_surf.get_rect()
    #         text_rect.center = (int(config.WINDOW_COLS*0.5), int(config.WINDOW_ROWS*0.875))
    #         print("The game is a draw!")

    #         while True:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.quit()
    #                     sys.exit()

    #             self.WINDOW_SURF.blit(text_surf, text_rect)
    #             self.main_clock.tick(config.FPS)
    #             pygame.display.update()

    #     else:
    #         text_surf = BIG_FONT.render('The game is over', True, config.BLACK)
    #         text_rect = text_surf.get_rect()
    #         text_rect.center = (int(config.WINDOW_COLS*0.5), int(config.WINDOW_ROWS*0.875))

    #         winner_surf = BIG_FONT.render(winner_str + '  Win!', True, config.BLACK)
    #         winner_rect = winner_surf.get_rect()
    #         winner_rect.center = (int(config.WINDOW_COLS*0.25), int(config.WINDOW_ROWS*0.9375))
        
    #         # loser_surf = BIG_FONT.render(loser_str + '  Lose~~', True, config.BLACK)
    #         # loser_rect = loser_surf.get_rect()
    #         # loser_rect.center = (int(config.WINDOW_COLS*0.75), int(config.WINDOW_ROWS*0.9375))
    #     print("Winner: ", winner_str)

    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()

    #         self.WINDOW_SURF.blit(text_surf, text_rect)
    #         self.WINDOW_SURF.blit(winner_surf, winner_rect)
    #         #self.WINDOW_SURF.blit(loser_surf, loser_rect)
    #         #show_statistics()
    #         self.main_clock.tick(config.FPS)
    #         pygame.display.update()

        