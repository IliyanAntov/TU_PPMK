import os

import pygame

from Game import Game


class Player(pygame.sprite.Sprite):

    def __init__(self):
        self.size = (64, 64)
        self.default_pos = (368, 700)
        self.speed = 5

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, -0.2)

        pygame.sprite.Sprite.__init__(self)

        player_image = pygame.image.load(os.path.join('imgs', 'player.png'))
        self.image = pygame.transform.scale(player_image, self.size)

        self.rect = self.image.get_rect()
        self.rect.left = self.default_pos[0]
        self.rect.top = self.default_pos[1]

    def draw(self):
        Game.screen.blit(self.image, self.rect)

    def move(self, dx, dy, frame_time):
        self.velocity
        self.movement_vector.length(math.sqrt(dx**2 + dy**2))
        new_x = self.rect.x + dx * frame_time / 100
        new_y = self.rect.y + dy * frame_time / 100
        if 0 <= new_x <= (Game.display_size.x - self.rect.width):
            self.rect.x = new_x
        if 0 <= new_y <= (Game.display_size.y - self.rect.height):
            self.rect.y = new_y

