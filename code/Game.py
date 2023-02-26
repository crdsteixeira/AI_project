import pygame
import sys
import main


class InitialScreen:
    def __init__(self):
        self.human_player = None
        self.computer_player = None
        self.titles = {
            'Which game mode do you want to chose?': ["Human vs Human", "Computer vs Human", "Computer vs Computer"],
            'In which board size would you like to play with?': ["3 X 3", "5 X 5", "5 X 9"],
            'What is your difficulty level?': ["Easy", "Medium", "Hard"],
            'White always goes first. Do you want to be white or black?': ["White", "Black"],
        }
        self.selected_options = {}

    def draw_option(self, title, options, y):
        # Choose game mode
        text = main.BIG_FONT.render(title, True, main.BLACK)
        rect = text.get_rect()
        rect.center = (int(main.WINDOW_WIDTH * 0.5), int(main.WINDOW_HEIGHT * y))

        text_list = []
        delta_x = 1./(len(options)+1)
        x = delta_x
        text_list.append((text, rect, title, False, False))
        for opt in options:
            surf = main.BIG_FONT.render(opt, True, main.BLACK)
            rect = surf.get_rect()
            rect.center = (int(main.WINDOW_WIDTH * x), int(main.WINDOW_HEIGHT * (y + 0.1)))
            selected = self.selected_options.get(title, None) == opt
            text_list.append((surf, rect, opt, selected, True))
            x += delta_x

        return text_list

    def draw_all_options(self):
        y = 0.1
        delta_y = (1 / len(self.titles))
        text_list = []
        for key, value in self.titles.items():
            text_list.append(self.draw_option(key, value, y))
            y += delta_y

        return text_list

    def draw_initial_screen(self):
        """Draws the text and handles the mouse click events for letting
        the player choose which color they want to be.
        Returns [WHITE_TOKEN, BLACK_TOKEN] if the player chooses to be White,
        [BLACK_TOKEN, WHITE_TOKEN] if Black.
        """
        text_list = self.draw_all_options()

        while True:  # keep looping until the player has clicked on a color
            main.main_clock.tick(main.FPS)  # CPU is too fast that slowing down is needed
            main.WINDOW_SURF.fill(main.WHITE)
            for opt in text_list:
                for i, (surf, rect, text, selected, selectable) in enumerate(opt):
                    color = main.GREEN if selected else main.BLACK # change text color based on selection status
                    if selectable:
                        new_surf = main.BIG_FONT.render(text, True, color)
                        main.WINDOW_SURF.blit(new_surf, rect)
                        opt[i] = (new_surf, rect, text, selected, selectable)  # update the text_list to reflect changes
                    else:
                        main.WINDOW_SURF.blit(surf, rect)
            for event in pygame.event.get():  # event handling loop
                main.main_clock.tick(main.FPS)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == main.MOUSEBUTTONDOWN and event.button == 1:
                    # print 'click'
                    mouse_x, mouse_y = event.pos
                    for opt in text_list:
                        for i, (surf, rect, text, selected, selectable) in enumerate(opt):
                            if rect.collidepoint((mouse_x, mouse_y)) and selectable:
                                self.selected_options[opt[0][2]] = opt[i][2]  # update selected option
                                for j, (s, r, t, sel, sela) in enumerate(opt):
                                    opt[j] = (s, r, t, t == opt[i][2], True)  # update other options
            main.main_clock.tick(main.FPS)
            pygame.display.update()
            main.main_clock.tick(main.FPS)
