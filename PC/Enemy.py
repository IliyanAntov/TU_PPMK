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

    def __init__(self, spawn_x: int, spawn_y: int):
        pygame.sprite.Sprite.__init__(self)

        self.size = Enemy.default_size
        self.image = pygame.transform.scale(Enemy.image, self.size)
        self.speed = Enemy.default_speed
        self.projectiles = []

        self.rect = self.image.get_rect()
        self.rect.topleft = (spawn_x, spawn_y)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)

    def draw(self, frame_time: int):
        # Generate a random number that will determine if the enemy will shoot this frame
        random_num = random.randint(0, 1 / Game.enemy_shoot_chance)
        # Only shoot a projectile if the generated number is 0
        if random_num == 0:
            # Create a red projectile in the bottom middle of the enemy
            projectile = Projectile(self.rect.midbottom[0], self.rect.midbottom[1])
            projectile.color = (255, 0, 0)
            self.projectiles.append(projectile)

        # Move all previously shot projectiles down
        for projectile in list(self.projectiles):
            projectile_destroyed = projectile.move(frame_time, "down")
            # If the projectile was destroyed (reached the end of the screen/hit player), remove it from the list
            if projectile_destroyed:
                self.projectiles.remove(projectile)
            # Display the projectile
            projectile.draw()

        # Draw the enemy on the screen
        Game.screen.blit(self.image, self.rect)

    def move(self, dx: int, dy: int, frame_time: int):
        # Create a vector pointing to the direction of travel
        movement_vector = pygame.math.Vector2(dx, dy)
        if movement_vector.length() == 0:
            return

        # Scale the vector based on the movement speed of the entity and the frame time (to ensure constant speed)
        movement_vector.scale_to_length(self.speed * (frame_time / 1000))
        # Move the position based on the vector
        self.pos.x += movement_vector.x
        self.pos.y += movement_vector.y

        # Restrict X movement to the game screen
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > (Game.display_size.x - self.rect.width):
            self.pos.x = (Game.display_size.x - self.rect.width)
        # Restrict Y movement to the game screen
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > (Game.display_size.y - self.rect.height):
            self.pos.y = (Game.display_size.y - self.rect.height)

        # Move the enemy to the new position
        self.rect.topleft = self.pos
