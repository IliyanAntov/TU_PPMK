import pygame

from Game import Game


class Projectile:
    default_size = (5, 10)
    default_color = (255, 255, 255)
    default_speed = 400

    def __init__(self, pos_x: int, pos_y: int):
        self.size = Projectile.default_size
        self.color = Projectile.default_color
        self.speed = Projectile.default_speed

        self.pos = pygame.math.Vector2(pos_x, pos_y)

        self.rect = pygame.rect.Rect(pos_x, pos_y, self.size[0], self.size[1])

    def draw(self):
        # Draw the projectile on the screen
        pygame.draw.rect(surface=Game.screen,
                         color=self.color,
                         rect=self.rect)

    def move(self, frame_time: int, direction: str) -> bool:
        # Move the projectile up based on the movement speed of the entity and the frame time (to ensure constant speed)
        if direction == "up":
            self.pos.y -= self.speed * (frame_time / 1000)
        # Move the projectile down based on the movement speed of the entity and the frame time (to ensure constant speed)
        elif direction == "down":
            self.pos.y += self.speed * (frame_time / 1000)

        # Restrict Y movement to the game screen
        if self.pos.y < 0 or self.pos.y > Game.display_size.y:
            return True

        # Move the projectile to the new position
        self.rect.top = self.pos.y
        return False
