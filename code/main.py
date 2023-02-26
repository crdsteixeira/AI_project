import pygame
import sys
from pygame.locals import *
from copy import deepcopy
import Board
import Player
from Game import InitialScreen

# -------------------------------------------------- CONSTANTS --------------------------------------------------------#
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

screen = InitialScreen()
screen.draw_initial_screen()
