import os
import random

import pygame

from Game import Game
from Projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    size = (16*4, 10*4)
    default_pos = (0, 0)
    min_x = Game.display_size.x / 4
    max_x = min_x * 3
    min_y = 0
    max_y = 3 * Game.display_size.y / 4
    movement_speed = 20

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        enemy_image = pygame.image.load(os.path.join('imgs', 'enemy.png'))
        self.size = Enemy.size
        self.image = pygame.transform.scale(enemy_image, self.size)

        self.rect = self.image.get_rect()
        self.rect.left = Enemy.default_pos[0]
        self.rect.top = Enemy.default_pos[1]

        self.projectiles = []

    def draw(self, frame_time):
        random_num = random.randint(0, 1 / Game.enemy_shoot_chance)
        if random_num == 0:
            projectile = Projectile(self.rect.midbottom[0], self.rect.midbottom[1])
            projectile.color = (255, 0, 0)
            self.projectiles.append(projectile)

        for projectile in list(self.projectiles):

            projectile_destroyed = projectile.move(frame_time, "down")
            if projectile_destroyed:
                self.projectiles.remove(projectile)
            projectile.draw()

        Game.screen.blit(self.image, self.rect)

    def move(self, dx, dy, frame_time):
        new_x = self.rect.x + dx * frame_time / 100
        new_y = self.rect.y + dy * frame_time / 100
        if 0 <= new_x <= (Game.display_size.x - self.rect.width):
            self.rect.x = new_x
        if 0 <= new_y <= (Game.display_size.y - self.rect.height):
            self.rect.y = new_y


