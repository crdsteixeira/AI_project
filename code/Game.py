from pygame.locals import *
from main import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
EMPTY = None


class InitialScreen:
    def __init__(self):
        self.human_player = None
        self.computer_player = None

        # Initialize pygame and the main clock
        pygame.init()
        self.main_clock = pygame.time.Clock()

        # Set up the window
        self.WINDOW_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Fanorona')
        self.SMALL_FONT = pygame.font.Font(None, 8)
        self.BIG_FONT = pygame.font.Font(None, 12)

    def draw_initial_screen(self):
        """Draws the text and handles the mouse click events for letting
        the player choose which color they want to be.
        Returns [WHITE_TOKEN, BLACK_TOKEN] if the player chooses to be White,
        [BLACK_TOKEN, WHITE_TOKEN] if Black.
        """
        gamemode_choice = None
        difficulty_choice = None
        token_choice = None
        board_choice = None

        # Choose game mode
        text_gamemode = self.BIG_FONT.render('Which game mode do you want to chose?', True, BLACK)
        text_gamemode_rect = text_gamemode.get_rect()
        text_gamemode_rect.center = (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.1))

        hh = self.BIG_FONT.render('Human vs Human', True, BLACK)
        hh_rect = hh.get_rect()
        hh_rect.center = (int(WINDOW_WIDTH * 0.175), int(WINDOW_HEIGHT * 0.2))

        ch = self.BIG_FONT.render('Computer vs Human', True, BLACK)
        ch_rect = ch.get_rect()
        ch_rect.center = (int(WINDOW_WIDTH * 0.375), int(WINDOW_HEIGHT * 0.2))

        cc = self.BIG_FONT.render('Computer vs Computer', True, BLACK)
        cc_rect = cc.get_rect()
        cc_rect.center = (int(WINDOW_WIDTH * 0.625), int(WINDOW_HEIGHT * 0.2))

        # Choose board size
        text_boardsize = self.BIG_FONT.render('In which board size would you like to play with?', True, BLACK)
        text_boardsize_rect = text_boardsize.get_rect()
        text_boardsize_rect.center = (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.3))

        x33 = self.BIG_FONT.render('3 X 3', True, BLACK)
        x33_rect = x33.get_rect()
        x33_rect.center = (int(WINDOW_WIDTH * 0.175), int(WINDOW_HEIGHT * 0.4))

        x55 = self.BIG_FONT.render('5 x 5', True, BLACK)
        x55_rect = x55.get_rect()
        x55_rect.center = (int(WINDOW_WIDTH * 0.375), int(WINDOW_HEIGHT * 0.4))

        x59 = self.BIG_FONT.render('5 x 9', True, BLACK)
        x59_rect = x59.get_rect()
        x59_rect.center = (int(WINDOW_WIDTH * 0.625), int(WINDOW_HEIGHT * 0.4))

        # Choose difficulty
        text_diff = self.BIG_FONT.render('What is your difficulty level?', True, BLACK)
        text_diff_rect = text_diff.get_rect()
        text_diff_rect.center = (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.5))

        easy = self.BIG_FONT.render('Easy', True, BLACK)
        easy_rect = easy.get_rect()
        easy_rect.center = (int(WINDOW_WIDTH * 0.175), int(WINDOW_HEIGHT * 0.6))

        medium_surf = self.BIG_FONT.render('Medium', True, BLACK)
        medium_rect = medium_surf.get_rect()
        medium_rect.center = (int(WINDOW_WIDTH * 0.375), int(WINDOW_HEIGHT * 0.6))

        hard_surf = self.BIG_FONT.render('Hard', True, BLACK)
        hard_rect = hard_surf.get_rect()
        hard_rect.center = (int(WINDOW_WIDTH * 0.625), int(WINDOW_HEIGHT * 0.6))

        # Choose token color
        text_surf = self.BIG_FONT.render('White always goes first. Do you want to be white or black?', True, BLACK)
        text_surf_rect = text_surf.get_rect()
        text_surf_rect.center = (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.7))

        white_surf = self.BIG_FONT.render('White', True, BLACK)
        white_rect = white_surf.get_rect()
        white_rect.center = (int(WINDOW_WIDTH * 0.375), int(WINDOW_HEIGHT * 0.8))

        black_surf = self.BIG_FONT.render('Black', True, BLACK)
        black_rect = black_surf.get_rect()
        black_rect.center = (int(WINDOW_WIDTH * 0.625), int(WINDOW_HEIGHT * 0.8))

        while True:  # keep looping until the player has clicked on a color
            self.main_clock.tick(FPS)  # CPU is too fast that slowing down is needed
            for event in pygame.event.get():  # event handling loop
                self.main_clock.tick(FPS)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # print 'click'
                    mouse_x, mouse_y = event.pos
                    if white_rect.collidepoint((mouse_x, mouse_y)):
                        white_surf = self.BIG_FONT.render('White', True, GREEN)
                        token_choice = [WHITE, BLACK]
                    elif black_rect.collidepoint((mouse_x, mouse_y)):
                        black_surf = self.BIG_FONT.render('White', True, GREEN)
                        token_choice = [BLACK, WHITE]
                    elif hard_rect.collidepoint((mouse_x, mouse_y)):
                        difficulty_choice = 'hard'
                    elif medium_rect.collidepoint((mouse_x, mouse_y)):
                        difficulty_choice = 'medium'
                    elif easy_rect.collidepoint((mouse_x, mouse_y)):
                        difficulty_choice = 'easy'
                    elif x59_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'x59'
                    elif x55_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'x55'
                    elif x33_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'x33'
                    elif cc_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'cc'
                    elif ch_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'ch'
                    elif hh_rect.collidepoint((mouse_x, mouse_y)):
                        token_choice = 'hh'

            self.WINDOW_SURF.fill(WHITE)
            self.WINDOW_SURF.blit(text_gamemode, text_gamemode_rect)
            self.WINDOW_SURF.blit(hh, hh_rect)
            self.WINDOW_SURF.blit(ch, ch_rect)
            self.WINDOW_SURF.blit(cc, cc_rect)
            self.WINDOW_SURF.blit(text_boardsize, text_boardsize_rect)
            self.WINDOW_SURF.blit(x33, x33_rect)
            self.WINDOW_SURF.blit(x55, x55_rect)
            self.WINDOW_SURF.blit(x59, x59_rect)
            self.WINDOW_SURF.blit(text_diff, text_diff_rect)
            self.WINDOW_SURF.blit(easy, easy_rect)
            self.WINDOW_SURF.blit(medium_surf, medium_rect)
            self.WINDOW_SURF.blit(hard_surf, hard_rect)
            self.WINDOW_SURF.blit(text_surf, text_surf_rect)
            self.WINDOW_SURF.blit(white_surf, white_rect)
            self.WINDOW_SURF.blit(black_surf, black_rect)
            self.main_clock.tick(FPS)
            pygame.display.update()
            self.main_clock.tick(FPS)
