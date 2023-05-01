from collections import namedtuple

import pygame


class Game:
    # Set the maximum frames per second for the game
    max_fps = 1000
    # Set the display size in pixels
    Display = namedtuple("Display", "x y")
    display_size = Display(800, 800)
    # Set the game score
    score = 0
    # Set the chance for an enemy to shoot (coefficient)
    enemy_shoot_chance = 0.001

    # Create the game screen
    screen = pygame.display.set_mode(size=display_size)
