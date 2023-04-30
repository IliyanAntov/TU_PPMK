import pygame

from Game import Game
from Level import Level
from Player import Player


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # controller = Controller()
    # controller.connect()
    # controller_input_thread = threading.Thread(target=Controller.read_input, args=(controller,))
    # controller_input_thread.start()
    # controller_button_states = (controller.but1, controller.but2, controller.butj)

    player = Player()
    level = Level(1)
    # controller.write_score(Game.score)

    # Main loop
    while True:
        frame_time = clock.tick(Game.fps)

        # Check if the player was hit by an enemy projectile
        if level.check_player_hit(player):
            Level.game_over_dialog()
            Game.score = 0
            # controller.write_score(Game.score)
            level = Level(1)
            continue

        # Check if any enemies were hit by player projectiles
        for projectile in player.projectiles:
            hit = level.check_enemy_hit(projectile)
            if hit:
                player.projectiles.remove(projectile)
                if level.check_completion():
                    Game.score += level.num * 1000
                    # controller.write_score(Game.score)
                    level = Level(level.num + 1)
                    print(Game.score)
                    continue

        # Draw the player and all enemies on screen
        Game.screen.fill((0, 0, 0))
        level.move_enemies(frame_time)
        level.draw(frame_time)
        player.draw(frame_time)
        pygame.display.update()

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


if __name__ == "__main__":
    # call the main function
    main()
    # print(controller.read_until(b"\r\n"))
