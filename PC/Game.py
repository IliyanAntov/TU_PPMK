from collections import namedtuple

import pygame


class Game:
    fps = 1000
    Display = namedtuple("Display", "x y")
    display_size = Display(800, 800)
    score = 0
    enemy_shoot_chance = 0.001

    screen = pygame.display.set_mode(display_size)
