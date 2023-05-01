import tkinter
from tkinter import Tk, Button

import pygame

from Enemy import Enemy
from Game import Game
from Player import Player
from Projectile import Projectile


class Level:
    # Set the offset (in pixels) between enemies in the level
    enemy_offset = 10
    # Set the maximum number of enemies in a row
    enemy_row_length = 5

    def __init__(self, number: int):
        self.num = number
        # Set the initial movement direction of the enemies
        self.movement_direction = "right"
        # Spawn enemies according to the level number
        self.enemies = self.spawn_enemies(level_number=number,
                                          enemy_row_length=Level.enemy_row_length)

    def draw(self, frame_time: int):
        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw(frame_time)

    @staticmethod
    def spawn_enemies(level_number: int, enemy_row_length: int) -> list[Enemy]:
        # Create an empty list for Enemy objects
        enemies = []
        # Create a row of enemies for each level number
        for i in range(level_number):
            # Place the first enemy in the row at the minimum X
            current_x = Enemy.min_x
            # Place the first enemy in the row at the right Y position depending on the row number
            current_y = i * (Enemy.default_size[1] + Level.enemy_offset)

            # Create enemy objects for the current row
            for j in range(enemy_row_length):
                # Create an Enemy object and add it to the list
                enemy = Enemy(spawn_x=current_x,
                              spawn_y=current_y)
                enemies.append(enemy)

                # Move the spawn point for the next enemy
                current_x += Enemy.default_size[0] + Level.enemy_offset

        # Return the list of all enemies  in the level
        return enemies

    def move_enemies(self, frame_time: int):
        # If the enemies are currently moving right
        if self.movement_direction == "right":
            # Find the X of the rightmost enemy in the level and spawn a copy of it
            rightmost_enemy_x = self._find_rightmost_enemy_x()
            rightmost_enemy = Enemy(spawn_x=rightmost_enemy_x,
                                    spawn_y=0)
            # Move the copy of the rightmost enemy one more step right
            rightmost_enemy.move(dx=Enemy.default_speed,
                                 dy=0,
                                 frame_time=frame_time)

            # If the enemies have reached the end of the screen, move them one row down
            if rightmost_enemy.rect.right >= Game.display_size.x:
                for enemy in self.enemies:
                    enemy.pos.y += Enemy.default_size[1]
                    enemy.rect.top = enemy.pos.y
                # Change the direction of enemy travel
                self.movement_direction = "left"

            # If the enemies have not reached the end of the screen, move them one step right
            else:
                for enemy in self.enemies:
                    enemy.move(dx=Enemy.default_speed,
                               dy=0,
                               frame_time=frame_time)

        # If the enemies are currently moving left
        elif self.movement_direction == "left":
            # Find the X of the leftmost enemy in the level and spawn a copy of it
            leftmost_enemy_x = self._find_leftmost_enemy_x()
            leftmost_enemy = Enemy(spawn_x=leftmost_enemy_x,
                                   spawn_y=0)
            # Move the copy of the leftmost enemy one more step left
            leftmost_enemy.move(dx=-Enemy.default_speed,
                                dy=0,
                                frame_time=frame_time)

            # If the enemies have reached the end of the screen, move them one row down
            if leftmost_enemy.rect.left <= 0:
                for enemy in self.enemies:
                    enemy.pos.y += enemy.default_size[1]
                    enemy.rect.top = enemy.pos.y
                # Change the direction of enemy travel
                self.movement_direction = "right"

            # If the enemies have not reached the end of the screen, move them one step left
            else:
                for enemy in self.enemies:
                    enemy.move(dx=-Enemy.default_speed,
                               dy=0,
                               frame_time=frame_time)

    def _find_leftmost_enemy_x(self) -> int:
        # Find the X of the current leftmost enemy rectangle and return it
        min_x = min(enemy.rect.x for enemy in self.enemies)
        return min_x

    def _find_rightmost_enemy_x(self) -> int:
        # Find the X of the current rightmost enemy rectangle and return it
        max_x = max(enemy.rect.x for enemy in self.enemies)
        return max_x

    def check_enemy_hit(self, projectile: Projectile) -> bool:
        # Iterate through the list of enemies in the level
        for enemy in self.enemies:
            # If the projectile has collided with an enemy, destroy the enemy and return True
            if enemy.rect.colliderect(projectile):
                self.enemies.remove(enemy)
                return True

        # If no collision was detected, return False
        return False

    def check_player_hit(self, player: Player):
        # Iterate through the list of enemies in the level
        for enemy in self.enemies:
            # If the player has collided with an enemy, return True
            if enemy.rect.colliderect(player):
                return True

        # Iterate through the list of enemies in the level
        for enemy in self.enemies:
            # Iterate through the list of projectiles for each enemy
            for projectile in enemy.projectiles:
                # If the player has collided with a projectile, return True
                if projectile.rect.colliderect(player):
                    return True

        # If no collision was detected, return False
        return False

    def check_completion(self):
        # If no enemies are left in the level, return True
        if not self.enemies:
            return True
        # If there are still non-destroyed enemies in the level, return False
        else:
            return False

    @staticmethod
    def game_over_dialog():
        # Create the dialog box window
        dialog_root = Tk()
        dialog_root.title("Game Over!")
        dialog_root.geometry("400x100")

        # Create a label with the game over text
        game_over = tkinter.Label(dialog_root, text="Game over! Try again?", font=("Arial", 22))
        game_over.pack(padx=10, fill=tkinter.X, expand=True)
        # Create a retry button that closes the dialog box
        retry_button = Button(dialog_root, text="Retry", command=dialog_root.destroy)
        retry_button.pack(padx=10, pady=10, fill=tkinter.X, side=tkinter.LEFT, expand=True)
        # Create a quit button that exits the game
        quit_button = Button(dialog_root, text="Quit", command=(lambda: Level.game_over(dialog_root)))
        quit_button.pack(padx=10, pady=10, fill=tkinter.X, side=tkinter.RIGHT, expand=True)

        # Display the dialog and wait for input
        dialog_root.mainloop()

    @staticmethod
    def game_over(tkinter_root):
        # Close the tkinter GUI
        tkinter_root.quit()
        # Close the pygame window
        pygame.quit()
        # Exit the program
        exit()
