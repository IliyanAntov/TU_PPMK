import threading

import numpy
import pygame

from Controller import Controller
from Enemy import Enemy
from Game import Game
from Player import Player


# define a main function
def main():

    pygame.init()
    player = Player()
    player.draw()

    enemy = Enemy()
    enemy.draw()

    clock = pygame.time.Clock()

    controller = Controller()
    controller.connect()
    controller_input_thread = threading.Thread(target=Controller.read_input, args=(controller,))
    controller_input_thread.start()

    while True:
        frame_time = clock.tick(Game.fps)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        x_move = numpy.interp(controller.x, [0, 4096], [-2048, 2048])
        y_move = numpy.interp(controller.y, [0, 4096], [-2048, 2048])
        player.move(x_move, -y_move, frame_time)

        if keys[pygame.K_a]:
            player.move(-50, 0, frame_time)
        if keys[pygame.K_d]:
            player.move(50, 0, frame_time)
        if keys[pygame.K_s]:
            player.move(0, 50, frame_time)
        if keys[pygame.K_w]:
            player.move(0, -50, frame_time)
        if keys[pygame.K_q]:
            pygame.quit()

        Game.screen.fill((0, 0, 0))
        player.draw()
        enemy.draw()
        pygame.display.update()


if __name__ == "__main__":
    # call the main function
    main()
    # print(controller.read_until(b"\r\n"))
