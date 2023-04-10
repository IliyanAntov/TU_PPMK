import threading

import numpy
import pygame

from Controller import Controller
from Enemy import Enemy
from Game import Game
from Player import Player


def main():

    pygame.init()
    player = Player()

    enemies = []
    for i in range(5):
        enemy = Enemy()
        enemy.rect.left += ((i * enemy.rect.width) + (i * 10))
        enemies.append(enemy)

    for enemy in enemies:
        enemy.draw()

    clock = pygame.time.Clock()

    controller = Controller()
    controller.connect()
    controller_input_thread = threading.Thread(target=Controller.read_input, args=(controller,))
    controller_input_thread.start()
    controller_button_states = (controller.but1, controller.but2, controller.butj)

    while True:
        frame_time = clock.tick(Game.fps)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.QUIT:
                controller.stop = True
                controller.disconnect()
                pygame.quit()
                exit()

        if controller.but2 == 0 and controller_button_states[1] != 0:
            player.shoot()
        x_move = numpy.interp(controller.x, [0, 4096], [-2048, 2048])
        y_move = numpy.interp(controller.y, [0, 4096], [-2048, 2048])
        controller_button_states = (controller.but1, controller.but2, controller.butj)

        player.move(x_move, -y_move, frame_time)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.move(-50, 0, frame_time)
        if keys[pygame.K_d]:
            player.move(50, 0, frame_time)
        if keys[pygame.K_s]:
            player.move(0, 50, frame_time)
        if keys[pygame.K_w]:
            player.move(0, -50, frame_time)

        Game.screen.fill((0, 0, 0))
        player.draw(frame_time)
        for enemy in enemies:
            enemy.draw()
        pygame.display.update()


if __name__ == "__main__":
    # call the main function
    main()
    # print(controller.read_until(b"\r\n"))
