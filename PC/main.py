import pygame

from Game import Game
from Level import Level
from Player import Player


def main():

    pygame.init()
    player = Player()

    clock = pygame.time.Clock()

    # controller = Controller()
    # controller.connect()
    # controller_input_thread = threading.Thread(target=Controller.read_input, args=(controller,))
    # controller_input_thread.start()
    # controller_button_states = (controller.but1, controller.but2, controller.butj)
    level = Level(1)
    while True:
        frame_time = clock.tick(Game.fps)

        level.move_enemies(frame_time)
        level.draw(frame_time)
        player.draw(frame_time)
        pygame.display.update()

        if level.check_player_hit(player):
            Game.score = 0

            Game.screen.fill((0, 0, 0))
            level = Level(1)
            level.draw(frame_time)
            player = Player()
            player.draw(frame_time)
            pygame.display.update()

            Level.game_over_dialog()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.QUIT:
                # controller.stop = True
                # controller.disconnect()
                pygame.quit()
                exit()

        # if controller.but2 == 0 and controller_button_states[1] != 0:
        #     player.shoot()
        #
        # x_move = numpy.interp(controller.x, [0, 4096], [-2048, 2048])
        # y_move = numpy.interp(controller.y, [0, 4096], [-2048, 2048])
        # controller_button_states = (controller.but1, controller.but2, controller.butj)

        # player.move(x_move, -y_move, frame_time)

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

        for projectile in player.projectiles:
            hit = level.check_enemy_hit(projectile)
            if hit:
                player.projectiles.remove(projectile)

        if level.check_completion():
            level = Level(level.num + 1)


if __name__ == "__main__":
    # call the main function
    main()
    # print(controller.read_until(b"\r\n"))
