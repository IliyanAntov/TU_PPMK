import os

import pygame

from Game import Game


class Enemy(pygame.sprite.Sprite):
    size = (64, 64)
    default_pos = (0, 0)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        enemy_image = pygame.image.load(os.path.join('imgs', 'player.png'))
        self.size = Enemy.size
        self.image = pygame.transform.scale(enemy_image, self.size)

        self.rect = self.image.get_rect()
        self.rect.left = Enemy.default_pos[0]
        self.rect.top = Enemy.default_pos[1]

    def draw(self):
        Game.screen.blit(self.image, self.rect)

    def move(self, dx, dy, frame_time):
        new_x = self.rect.x + dx * frame_time / 100
        new_y = self.rect.y + dy * frame_time / 100
        if 0 <= new_x <= (Game.display_size.x - self.rect.width):
            self.rect.x = new_x
        if 0 <= new_y <= (Game.display_size.y - self.rect.height):
            self.rect.y = new_y

