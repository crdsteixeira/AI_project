import pygame
import sys
from pygame.locals import *
from main import *
from Player import *
from copy import deepcopy


class Board:
    def __init__(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.grid_size = self.grid_width * self.grid_height
        self.grid = None
        self.token_colors = None
        self.human_token = None
        self.computer_token = None
        self.current_turn = None
        self.move_history = []

        if self.grid_width == 3 and self.grid_height == 3:
            img = '../images/ThreeByThree.png'
        elif self.grid_width == 5 and self.grid_height == 5:
            img = '../images/FiveByFive.png'
        else:
            img = '../images/EmptyBackground.png'

        self.BG_IMAGE = pygame.image.load(img)
        self.BG_IMAGE = pygame.transform.scale(self.BG_IMAGE, (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.5)))
        self.SMALL_FONT = pygame.font.Font(None, 20)
        self.BIG_FONT = pygame.font.Font(None, 40)


    def get_movable_token_information(self):
        pass


    def handle_click(self):
        human_movable_token_table = get_movable_token_information(human_token, main_grid)
        if human_movable_token_table == {}:
            show_game_results('AI', 'You Human')
        check_for_draw(main_grid, turn)

        click_grid_coord = None
        move_grid_coord = None
        while move_grid_coord == None:
            show_statistics()
            while click_grid_coord == None:
                main_clock.tick(FPS)
                for event in pygame.event.get():  # event handling loop
                    main_clock.tick(FPS)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        click_grid_coord = get_grid_clicked((mouse_x, mouse_y))
                        if click_grid_coord not in human_movable_token_table:
                            click_grid_coord = None

                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            # when grid got clicked, extra green circle shows it.
            pygame.draw.circle(
                WINDOW_SURF,
                GREEN,
                translate_grid_to_pixel_coord(click_grid_coord),
                int(GRID_SIZE * 0.5),
                10)

            main_clock.tick(FPS)
            pygame.display.update()
            main_clock.tick(FPS)

            # when a valid movable token got clicked, its accordingly available empty grid
            # coordinates start being detected.

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    move_grid_coord = get_grid_clicked((mouse_x, mouse_y))
                    if move_grid_coord not in human_movable_token_table[click_grid_coord]:
                        if move_grid_coord in human_movable_token_table:
                            click_grid_coord = move_grid_coord
                            move_grid_coord = None

                            draw_grid(main_grid)
                            pygame.draw.circle(
                                WINDOW_SURF,
                                GREEN,
                                translate_grid_to_pixel_coord(click_grid_coord),
                                int(GRID_SIZE * 0.5),
                                10)

                            main_clock.tick(FPS)
                            pygame.display.update()
                            main_clock.tick(FPS)
                        else:
                            move_grid_coord = None

        make_move(human_token, main_grid, click_grid_coord, move_grid_coord, True)


    def start(self):
        """Sets up the game state and begins the game loop."""

        # Set up the initial game state
        self.grid = self.get_initial_grid()
        self.token_colors = self.enter_player_token()
        self.human_token = self.token_colors[0]
        self.computer_token = self.token_colors[1]
        self.human_player = Player(self.human_token, self.grid_height, self.grid_width)
        self.computer_player = Player(self.computer_token, self.grid_height, self.grid_width)


        if self.human_token == WHITE:
            self.current_turn = self.human_token
        else:
            self.current_turn = self.computer_token

        # Begin the game loop
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click()

            # Draw the game board
            self.draw_grid(self.grid)

            # Check if the game is over
            if self.is_game_over():
                self.handle_game_over()

            # Update the screen
            pygame.display.update()
            main_clock.tick(FPS)

    def get_initial_grid(self):
        """Returns a 2D array representing the initial state of the game board."""

        grid = [[{'token_color': EMPTY, 'displacements': []} for _ in range(self.GRID_HEIGHT)] for _ in range(self.GRID_WIDTH)]

        # Set up the tokens for the white player
        for column in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if column % 2 == 1 and row % 2 == 0:
                    grid[column][row]['token_color'] = WHITE
                    grid[column][row]['displacements'] = self.get_displacements(column, row)

        # Set up the tokens for the black player
        for column in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if column % 2 == 0 and row % 2 == 1:
                    grid[column][row]['token_color'] = BLACK
                    grid[column][row]['displacements'] = self.get_displacements(column, row)

        return grid

    def get_displacements(self, column, row):
            """Returns a list of tuples representing the valid moves for the token at
            the specified column and row.
            """
            token_color = self.grid[column][row]['token_color']
            moves = []

            # Check all directions for valid moves
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Skip center position
                    x, y = column + dx, row + dy
                    if self.is_within_grid(x, y) and self.grid[x][y]['token_color'] == EMPTY:
                        # Single step move
                        moves.append(((column, row), (x, y)))
                    x, y = column + 2*dx, row + 2*dy
                    if self.is_within_grid(x, y) and self.grid[x][y]['token_color'] == EMPTY:
                        # Capture move
                        # Check if there is an opponent's token in between
                        opp_color = BLACK_TOKEN if token_color == WHITE_TOKEN else WHITE_TOKEN
                        if (dx == 1 and dy == 0 and self.grid[column+1][row]['token_color'] == opp_color) or \
                           (dx == -1 and dy == 0 and self.grid[column-1][row]['token_color'] == opp_color) or \
                           (dx == 0 and dy == 1 and self.grid[column][row+1]['token_color'] == opp_color) or \
                           (dx == 0 and dy == -1 and self.grid[column][row-1]['token_color'] == opp_color):
                            moves.append(((column, row), (x, y)))

            return moves

