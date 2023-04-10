from collections import namedtuple

import pygame


class Game:

    fps = 1000
    Display = namedtuple("Display", "x y")
    display_size = Display(800, 800)

    screen = pygame.display.set_mode(display_size)
