from numpy import size
import pygame
import sys
from pygame.locals import *
#from main import *
#from Player import *
from copy import deepcopy


#color         R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
RED        = (255,   0,   0)
EMPTY      = 'EMPTY'  # nothing to draw on the grid

WINDOW_WIDTH = 800  # width of the program's window, in pixels
WINDOW_HEIGHT = 800  # height in pixels

class Board:

    def __init__(self, cols, rows):
        self.GRID_SIZE = 50  # size of the beads
        self.GRID_COLS = cols  # how many columns of grid on the game board
        self.GRID_ROWS = rows  # how many rows of spaces on the game board

        # if self.GRID_COLS == 3:
        #     img = '../images/ThreeByThree.png'
        # elif self.GRID_COLS == 5:
        #     img = '../images/FiveByFive.png'
        # elif self.GRID_COLS == 9:
        #     img = '../images/NineByFive.png'

        # self.BG_IMAGE = pygame.image.load(img)
        # self.BG_IMAGE = pygame.transform.scale(self.BG_IMAGE, (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.5)))
        # self.SMALL_FONT = pygame.font.Font(None, 20)
        # self.BIG_FONT = pygame.font.Font(None, 40)



    def get_new_grid(GRID_COLS, GRID_ROWS):
        """Returns a 2-dimensional array of token information.
        The first/second array index means column/row number that count from zero.
        Each token information is a hash table containing its token color and
        displacements of all adjacent grid positions.
        """

        grid = []
        for i in range(GRID_COLS):
            grid.append([])

        for coloumn in grid:
            for i in range(GRID_ROWS):
                coloumn.append({'token_color': EMPTY,
                                'displacements': []})
        
        # initialize grid positions with different displacements of
        # all adjacent grid positions

        # 3 X 3
        if GRID_COLS == 3 :  

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
        if GRID_COLS == 5 : 

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
        if GRID_COLS == 9 :
            _ = 0
        

        print(grid)
        return grid

    
    def get_movable_token_information(token_color, grid, is_prompt_bi_direct_capture=True):
        """returns a hash table that hashes each movable token
        coordinate to its own hash table consisting of each accordingly available
        empty grid coordinates to move hashing to its move type.
        """
        capture_move_table = {}
        paika_move_table = {}
        has_capture = False  # a flag shows which table to return

        GRID_COLS = len(grid)
        GRID_ROWS = int(size(grid)/GRID_COLS)

        for column in range(GRID_COLS):  
            for row in range(GRID_ROWS): 
                if grid[column][row]['token_color'] == token_color:
                    paika_move_table[(column, row)] = {}
                    capture_move_table[(column, row)] = {}
                    for (delta_x, delta_y) in grid[column][row]['displacements']:

                        # when a token's neighbor is EMPTY, it at least eligible for Paika move
                        # only after a token in Paika list, it will be test for what kind of
                        # capture it fits within the boundary of grid.

                        if grid[column + delta_x][row + delta_y]['token_color'] == EMPTY:
                            paika_move_table[(column, row)][(column + delta_x, row + delta_y)] = 'paika'

                            if Board.is_within_grid(column + 2*delta_x, row + 2*delta_y, GRID_COLS, GRID_ROWS) and \
                                grid[column + 2*delta_x][row + 2*delta_y]['token_color']\
                                    != token_color and \
                                        grid[column + 2*delta_x][row + 2*delta_y]['token_color']\
                                            != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)]\
                                    = 'approach'
                                has_capture = True

                                if  is_prompt_bi_direct_capture and \
                                        Board.is_within_grid(column - delta_x, row - delta_y, GRID_COLS, GRID_ROWS) and \
                                            grid[column - delta_x][row - delta_y]['token_color']\
                                                != token_color and \
                                                    grid[column - delta_x][row - delta_y]\
                                                        ['token_color'] != EMPTY:
                                    capture_move_table[(column, row)][(column + delta_x, row + delta_y)]\
                                        = 'bi-direction'

                            elif Board.is_within_grid(column - delta_x, row - delta_y, GRID_COLS, GRID_ROWS) and \
                                    grid[column - delta_x][row - delta_y]['token_color']\
                                        != token_color and \
                                            grid[column - delta_x][row - delta_y]['token_color']\
                                                != EMPTY:
                                capture_move_table[(column, row)][(column + delta_x, row + delta_y)]\
                                        = 'withdraw'
                                has_capture = True

        if has_capture:
            result_table = Board.clean_table(capture_move_table)
            print(('get from movable token information\ncapture table  ', result_table, '\n'))
            return result_table

        else:
            result_table = Board.clean_table(paika_move_table)
            print(('get from movable token information\npaika table  ', result_table, '\n'))
            return result_table
    
        
    def is_within_grid(x, y, GRID_COLS, GRID_ROWS):
        return x >= 0 and x < GRID_COLS and y >= 0 and y < GRID_ROWS
    
    def clean_table(move_table):
    # return a cleaned move table that only consists of valid move.
        new_table = {k: v for k, v in move_table.items() if v != {} }
        return new_table
    
    



"""
        
        self.grid_width = width
        self.grid_height = height
        self.grid_size = self.grid_width * self.grid_height
        self.grid = None
        self.token_colors = None
        self.human_token = None
        self.computer_token = None
        self.current_turn = None
        self.move_history = []



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
        #Sets up the game state and begins the game loop

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
        #Returns a 2D array representing the initial state of the game board

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
            #Returns a list of tuples representing the valid moves for the token at
            #the specified column and row.
            
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

"""