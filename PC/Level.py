import copy
import itertools
import math

from Enemy import Enemy
from Game import Game


class Level:
    enemy_offset = 10

    def __init__(self, number):
        self.num = number
        self.enemies = []
        self.enemy_row_length = 5
        self.movement_direction = "right"
        self.spawn_enemies()

    def draw(self, frame_time):
        for enemy in itertools.chain.from_iterable(self.enemies):
            enemy.draw(frame_time)

    def spawn_enemies(self):
        for i in range(self.num):
            enemy = Enemy()
            self.enemies.append([])
            current_x = Enemy.min_x
            current_y = i * (enemy.rect.height + Level.enemy_offset)

            for j in range(self.enemy_row_length):
                enemy = Enemy()

                enemy.rect.x = current_x
                enemy.rect.y = current_y

                current_x += enemy.rect.width + Level.enemy_offset

                self.enemies[i].append(enemy)

    def move_enemies(self, frame_time):

        if self.movement_direction == "right":
            # If the enemies have reached the end of the screen, move them one row down
            last_enemy = self._find_last_enemy()
            last_enemy.move(dx=Enemy.movement_speed,
                            dy=0,
                            frame_time=frame_time)

            if last_enemy.rect.right >= Game.display_size.x:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.rect.top += (enemy.rect.height + Level.enemy_offset)
                self.movement_direction = "left"
            # If the enemies have not reached the end of the screen, move them right
            else:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.move(dx=Enemy.movement_speed,
                               dy=0,
                               frame_time=frame_time)

        elif self.movement_direction == "left":
            first_enemy = self._find_first_enemy()
            first_enemy.move(dx=-Enemy.movement_speed,
                             dy=0,
                             frame_time=frame_time)

            # If the enemies have reached the end of the screen, move them one row down
            if first_enemy.rect.left <= 0:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.rect.top += (enemy.rect.height + Level.enemy_offset)
                    self.movement_direction = "right"
            # If the enemies have not reached the end of the screen, move them right
            else:
                for enemy in itertools.chain.from_iterable(self.enemies):
                    enemy.move(dx=-Enemy.movement_speed,
                               dy=0,
                               frame_time=frame_time)

    def _find_first_enemy(self):
        first_enemy_found = None
        for i in range(len(self.enemies)):
            if not self.enemies[i]:
                continue
            first_enemy = Enemy()
            first_enemy.rect.x = self.enemies[i][0].rect.x
            first_enemy.rect.y = self.enemies[i][0].rect.y

            if first_enemy_found is None or first_enemy.rect.x < first_enemy_found.rect.x:
                first_enemy_found = first_enemy

        return first_enemy_found

    def _find_last_enemy(self):
        last_enemy_found = None
        for i in range(len(self.enemies)):
            if not self.enemies[i]:
                continue
            last_enemy = Enemy()
            last_enemy.rect.x = self.enemies[i][-1].rect.x
            last_enemy.rect.y = self.enemies[i][-1].rect.y

            if last_enemy_found is None or last_enemy.rect.x > last_enemy_found.rect.x:
                last_enemy_found = last_enemy

        return last_enemy_found

    def check_projectile_collisions(self, projectile):
        for i in range(len(self.enemies)):
            for j in range(len(self.enemies[i])):
                if self.enemies[i][j].rect.colliderect(projectile):
                    self.enemies[i].remove(self.enemies[i][j])
                    return True
        return False

    def check_player_collision(self, player):
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
