import threading
from collections import namedtuple

import numpy
import pygame

from Controller import Controller
from Game import Game
from Level import Level
from Player import Player


def main():
    # Initialize the pygame module and clock
    pygame.init()
    clock = pygame.time.Clock()

    # Initialize the controller module
    controller = Controller()
    # Connect to the controller
    controller.connect()
    # Create a thread for reading of controller input
    controller_input_thread = threading.Thread(target=Controller.read_input, args=(controller,))
    controller_input_thread.start()
    # Save the current states of all controller buttons
    ButtonStates = namedtuple("ButtonStates", "but1, but2, butj")
    controller_button_states = ButtonStates(controller.but1, controller.but2, controller.butj)

    # Initialize the player module
    player = Player()
    # Load the first level
    level = Level(1)
    # Write the game score to the controller
    controller.write_score(Game.score)

    # Main loop
    while True:
        # Get the time it took to render the previous frame
        frame_time = clock.tick(Game.max_fps)

        # Check if the player was hit by an enemy projectile
        if level.check_player_hit(player):
            # Display the game over dialog
            Level.game_over_dialog(controller)
            # If the "Retry" button was pressed, reset the score and write it to the controller
            Game.score = 0
            controller.write_score(Game.score)
            # Load the first level
            level = Level(1)
            # Go to the next iteration of the main loop
            continue

        # Check if any enemies were hit by player projectiles
        for projectile in player.projectiles:
            hit = level.check_enemy_hit(projectile)
            if hit:
                # Destroy the player projectile
                player.projectiles.remove(projectile)
                # Check if the level was completed
                if level.check_completion():
                    # Increase the score and write it to the controller
                    Game.score += level.num * 1000
                    controller.write_score(Game.score)
                    # Load the next level
                    level = Level(level.num + 1)
                    # Empty the list of player projectiles
                    player.projectiles = []
                    # Go to the next iteration of the main loop
                    continue

        # Draw the player, enemies and projectiles on the game screen
        Game.screen.fill((0, 0, 0))
        level.move_enemies(frame_time)
        level.draw(frame_time)
        player.draw(frame_time)
        # Display the new frame
        pygame.display.update()

        # Get a list of pygame events
        events = pygame.event.get()
        for event in events:
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         player.shoot()

            # If the "QUIT" event was received
            if event.type == pygame.QUIT:
                # Stop the input thread
                controller.stop = True
                # Disconnect the controller
                controller.disconnect()
                # Close the pygame window
                pygame.quit()
                # Exit the program
                exit()

        # Save the current states of all controller buttons
        controller_button_states = (controller.but1, controller.but2, controller.butj)

        # If the "shoot" button was pressed (where it was not previously), shoot a projectile from the player
        if controller.but2 == 0 and controller_button_states[1] != 0:
            player.shoot()

        # Map the X and Y movement values received from the controller (numbers between 0 and 4096) to values used by
        # the player movement function (numbers between -2048 and 2048)
        x_move = numpy.interp(controller.x, [0, 4096], [-2048, 2048])
        y_move = numpy.interp(controller.y, [0, 4096], [-2048, 2048])
        # Move the player according to the input received from the controller
        player.move(dx=x_move,
                    dy=-y_move,
                    frame_time=frame_time)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_a]:
        #     player.move(-50, 0, frame_time)
        # if keys[pygame.K_d]:
        #     player.move(50, 0, frame_time)
        # if keys[pygame.K_s]:
        #     player.move(0, 50, frame_time)
        # if keys[pygame.K_w]:
        #     player.move(0, -50, frame_time)


if __name__ == "__main__":
    # Call the main function
    main()
