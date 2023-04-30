import pygame

from Game import Game


class Projectile:
    def __init__(self, pos_x, pos_y):
        self.size = (5, 10)
        self.color = (255, 255, 255)
        self.speed = 400
        self.pos = pygame.math.Vector2(pos_x, pos_y)

        self.rect = pygame.rect.Rect(pos_x, pos_y, self.size[0], self.size[1])

    def draw(self):
        pygame.draw.rect(Game.screen, self.color, self.rect)

    def move(self, frame_time, direction):
        if direction == "up":
            self.pos.y -= self.speed * (frame_time / 1000)
        elif direction == "down":
            self.pos.y += self.speed * (frame_time / 1000)

        if self.pos.y < 0:
            return True

        self.rect.top = self.pos.y
        return False
