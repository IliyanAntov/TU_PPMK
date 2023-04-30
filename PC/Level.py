import copy
import itertools
import math
import tkinter
from tkinter import Tk, Button

import pygame

from Enemy import Enemy
from Game import Game


class Level:
    enemy_offset = 10

    def __init__(self, number):
        self.num = number
        self.enemy_row_length = 5
        self.movement_direction = "right"
        self.enemies = self.spawn_enemies()

    def draw(self, frame_time):
        for enemy in itertools.chain.from_iterable(self.enemies):
            enemy.draw(frame_time)

    def spawn_enemies(self):
        enemies = []
        for i in range(self.num):
            enemies.append([])
            current_x = Enemy.min_x
            current_y = i * (Enemy.size[1] + Level.enemy_offset)

            for j in range(self.enemy_row_length):

                enemy = Enemy(spawn_x=current_x,
                              spawn_y=current_y)

                enemies[i].append(enemy)

                current_x += Enemy.size[0] + Level.enemy_offset

        return enemies

    def move_enemies(self, frame_time):
        if self.movement_direction == "right":
            rightmost_enemy_x = self._find_rightmost_enemy_x()
            rightmost_enemy = Enemy(spawn_x=rightmost_enemy_x,
                                    spawn_y=0)

            rightmost_enemy.move(dx=Enemy.default_speed,
                                 dy=0,
                                 frame_time=frame_time)

            # If the enemies have reached the end of the screen, move them one row down
            if rightmost_enemy.rect.right >= Game.display_size.x:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.pos.y += Enemy.size[1]
                    enemy.rect.top = enemy.pos.y
                self.movement_direction = "left"

            # If the enemies have not reached the end of the screen, move them right
            else:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.move(dx=Enemy.default_speed,
                               dy=0,
                               frame_time=frame_time)

        elif self.movement_direction == "left":
            rightmost_enemy_x = self._find_leftmost_enemy_x()
            leftmost_enemy = Enemy(spawn_x=rightmost_enemy_x,
                                   spawn_y=0)

            leftmost_enemy.move(dx=Enemy.default_speed,
                                dy=0,
                                frame_time=frame_time)

            # If the enemies have reached the end of the screen, move them one row down
            if leftmost_enemy.rect.left <= 0:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.pos.y += Enemy.size[1]
                    enemy.rect.top = enemy.pos.y
                    self.movement_direction = "right"

            # If the enemies have not reached the end of the screen, move them right
            else:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.move(dx=-Enemy.default_speed,
                               dy=0,
                               frame_time=frame_time)

    def _find_leftmost_enemy_x(self):
        min_x = min(enemy.rect.x for enemy in itertools.chain.from_iterable(self.enemies))
        return min_x

    def _find_rightmost_enemy_x(self):
        max_x = max(enemy.rect.x for enemy in itertools.chain.from_iterable(self.enemies))
        return max_x

    def check_enemy_hit(self, projectile):
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies[i])):
                if self.enemies[i][j].rect.colliderect(projectile):
                    self.enemies[i].remove(self.enemies[i][j])
                    return True
        return False

    def check_player_hit(self, player):
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies[i])):
                if self.enemies[i][j].rect.colliderect(player):
                    return True

        for enemy in itertools.chain.from_iterable(self.enemies):
            for projectile in enemy.projectiles:
                if projectile.rect.colliderect(player):
                    return True

        return False

    def check_completion(self):
        if not any(self.enemies):
            return True
        else:
            return False

    @staticmethod
    def game_over_dialog():
        dialog_root = Tk()
        dialog_root.title("Game Over!")
        dialog_root.geometry("400x100")

        game_over = tkinter.Label(dialog_root, text="Game over! Try again?", font=("Arial", 22))
        retry_button = Button(dialog_root, text="Retry", command=(lambda: Level.retry(dialog_root)))
        quit_button = Button(dialog_root, text="Quit", command=(lambda: Level.game_over(dialog_root)))

        game_over.pack(padx=10, fill=tkinter.X, expand=True)
        retry_button.pack(padx=10, pady=10, fill=tkinter.X, side=tkinter.LEFT, expand=True)
        quit_button.pack(padx=10, pady=10, fill=tkinter.X, side=tkinter.RIGHT, expand=True)

        dialog_root.mainloop()

    @staticmethod
    def retry(tkinter_root):
        tkinter_root.destroy()

    @staticmethod
    def game_over(tkinter_root):
        tkinter_root.quit()
        pygame.quit()
        exit()
