import os
import random

import pygame

from Game import Game
from Projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('imgs', 'enemy.png'))
    default_speed = 200
    default_size = (16 * 4, 10 * 4)
    default_pos = (0, 0)
    min_x = Game.display_size.x / 5

    def __init__(self, spawn_x, spawn_y):
        pygame.sprite.Sprite.__init__(self)

        self.size = Enemy.default_size
        self.image = pygame.transform.scale(Enemy.image, self.size)
        self.speed = Enemy.default_speed

        self.rect = self.image.get_rect()
        self.rect.topleft = (spawn_x, spawn_y)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)

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
        movement_vector = pygame.math.Vector2(dx, dy)
        if movement_vector.length() == 0:
            return

        movement_vector.scale_to_length(self.speed * (frame_time / 1000))
        self.pos.x += movement_vector.x
        self.pos.y += movement_vector.y

        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > (Game.display_size.x - self.rect.width):
            self.pos.x = (Game.display_size.x - self.rect.width)

        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > (Game.display_size.y - self.rect.height):
            self.pos.y = (Game.display_size.y - self.rect.height)

        self.rect.topleft = self.pos
