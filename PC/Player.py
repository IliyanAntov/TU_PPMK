import os

import pygame

from Game import Game
from Projectile import Projectile


class Player(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('imgs', 'player.png'))
    default_size = (16 * 4, 16 * 4)
    default_pos = (368, 700)
    default_speed = 400
    # Center deadzone for player movement to compensate for controller inaccuracy
    controller_deadzone = (-50, 50)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.size = Player.default_size
        self.image = pygame.transform.scale(Player.image, self.size)
        self.speed = Player.default_speed
        self.projectiles = []

        self.pos = pygame.math.Vector2(Player.default_pos[0], Player.default_pos[1])

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos.x, self.pos.y

    def draw(self, frame_time: int):
        # Move all previously shot projectiles up
        for projectile in list(self.projectiles):
            projectile_destroyed = projectile.move(frame_time, "up")
            # If the projectile was destroyed (reached the end of the screen/hit enemy), remove it from the list
            if projectile_destroyed:
                self.projectiles.remove(projectile)
            # Display the projectile
            projectile.draw()

        # Draw the player on the screen
        Game.screen.blit(self.image, self.rect)

    def move(self, dx: int, dy: int, frame_time: int):
        # If the X movement is within the center deadzone, remove it
        if self.controller_deadzone[0] < dx < self.controller_deadzone[1]:
            dx = 0
        # If the Y movement is within the center deadzone, remove it
        if self.controller_deadzone[0] < dy < self.controller_deadzone[1]:
            dy = 0

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

        # Move the player to the new position
        self.rect.topleft = self.pos

    def shoot(self):
        # Create a white projectile in the top middle of the player
        projectile = Projectile(self.rect.midtop[0], self.rect.midtop[1])
        self.projectiles.append(projectile)
