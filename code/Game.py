import pygame
import sys
import config


class Screen:
    def __init__(self, WINDOW_SURF, main_clock, FONT):
        self.titles = {
            'mode': {'Which game mode do you want to chose?': ["Human vs Human", "Computer vs Human",
                                                               "Computer vs Computer"]},
            'size': {'In which board size would you like to play with?': ["3 X 3", "5 X 5", "9 X 5"]},
            'difficulty': {'What is your difficulty level?': ["Easy", "Medium", "Hard"]},
            'token': {'White always goes first. Do you want to be white or black?': ["White", "Black"]},
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
            rect.center = (int(config.WINDOW_WIDTH * x), int(config.WINDOW_HEIGHT * (y + 0.1)))
            selected = self.selected_options.get(key, None) == opt
            text_list.append((key, surf, rect, opt, selected, True))
            x += delta_x

        return text_list

    def draw_all_options(self):
        y = 0.1
        delta_y = (1 / len(self.titles))
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

            # blit the button surface onto the screen surface
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

    def draw_grid(self, grid, board):
        if board.GRID_COLS == 3:
            BG_IMAGE = pygame.image.load('./images/ThreeByThree.png')
        if board.GRID_COLS == 5:
            BG_IMAGE = pygame.image.load('./images/FiveByFive.png')
        if board.GRID_COLS == 9:
            BG_IMAGE = pygame.image.load('./images/NineByFive.png')

        BG_IMAGE = pygame.transform.smoothscale(BG_IMAGE,
                                                (int(config.WINDOW_WIDTH * 0.5), int(config.WINDOW_HEIGHT * 0.5)))
        self.WINDOW_SURF.fill(config.WHITE)
        self.WINDOW_SURF.blit(
            BG_IMAGE,
            (int(config.WINDOW_WIDTH * 0.25), int(config.WINDOW_HEIGHT * 0.25)))

        for column in range(board.GRID_COLS):
            for row in range(board.GRID_ROWS):
                center_pixel_coord = self.translate_grid_to_pixel_coord((column, row), board)
                # draw token with outline
                if grid[column][row]['token_color'] != config.EMPTY:
                    pygame.draw.circle(
                        self.WINDOW_SURF,
                        grid[column][row]['token_color'],
                        center_pixel_coord,
                        int(board.GRID_SIZE * 0.5))

                    pygame.draw.circle(
                        self.WINDOW_SURF,
                        config.BLACK,
                        center_pixel_coord,
                        int(board.GRID_SIZE * 0.5),
                        2)

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
