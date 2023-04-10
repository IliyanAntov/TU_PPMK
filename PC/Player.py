import os

import pygame

from Game import Game


class Player(pygame.sprite.Sprite):

    def __init__(self):
        self.size = (64, 64)
        self.default_pos = (368, 700)
        self.speed = 400
        self.deadzone = (-50, 50)

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, -0.2)

        pygame.sprite.Sprite.__init__(self)

        player_image = pygame.image.load(os.path.join('imgs', 'player.png'))
        self.image = pygame.transform.scale(player_image, self.size)

        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(self.default_pos[0], self.default_pos[1])
        self.rect.topleft = self.pos.x, self.pos.y

    def draw(self):
        Game.screen.blit(self.image, self.rect)

    def move(self, dx, dy, frame_time):
        if self.deadzone[0] < dx < self.deadzone[1]:
            dx = 0
        if self.deadzone[0] < dy < self.deadzone[1]:
            dy = 0

        movement_vector = pygame.math.Vector2(dx, dy)
        if movement_vector.length() == 0:
            return

        movement_vector.scale_to_length(self.speed*(frame_time/1000))
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
