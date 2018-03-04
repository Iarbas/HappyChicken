#!/usr/bin/python

# Das folgende Programm ist ein Spiel, welches von Peppa Wutz stammt und den Namen traegt "Das lustige Huehnchen".
#
# Autor:  Andre Alexander Pieper.
# Version 1.0
# Datum:  01.02.2018
# Lizenz: LGPLv3

import os, sys, traceback, time, math, random
import pygame


def calc_position(end_position, old_position, distance_old, velocity, time_step, boundaries, step_size, propability,
                  right, lay_egg):

    position = old_position
    distance = math.sqrt((end_position[0] - old_position[0]) ** 2 + (end_position[1] - old_position[1]) ** 2)

    # Generation of a new end point.
    if distance < 0.5 or distance > distance_old:
        # Define a random share of the horizont and vertical move.
        step_share = random.random()

        # At first decide left or right
        if propability[0] < random.random():
            # Turn left.
            right = False
            end_position[0] = old_position[0] - math.sqrt((step_size ** 2) * step_share)

        else:
            # Turn right.
            right = True
            end_position[0] = old_position[0] + math.sqrt((step_size ** 2) * step_share)

        # Up or down
        if propability[1] < random.random():
            # Up.
            end_position[1] = old_position[1] - math.sqrt((step_size ** 2) * (1 - step_share))

        else:
            # Down.
            end_position[1] = old_position[1] + math.sqrt((step_size ** 2) * (1 - step_share))

    # Or go further.
    else:
        m = (old_position[1] - end_position[1]) / (old_position[0] - end_position[0])
        n = end_position[1] - end_position[0] * m

        d = velocity * time_step

        p = (2 * m * n - 2 * old_position[0] - 2 * m * old_position[1]) / (1 + m ** 2)
        q = (old_position[0] ** 2 + n ** 2 - 2 * n * old_position[1] + old_position[1] ** 2 - d ** 2) / (1 + m ** 2)

        tmp_x_1 = - p / 2 + math.sqrt((p / 2) ** 2 - q)
        tmp_x_2 = - p / 2 - math.sqrt((p / 2) ** 2 - q)

        tmp_y_1 = m * tmp_x_1 + n
        tmp_y_2 = m * tmp_x_2 + n

        d_1 = math.sqrt((end_position[0] - tmp_x_1) ** 2 + (end_position[1] - tmp_y_1) ** 2)
        d_2 = math.sqrt((end_position[0] - tmp_x_2) ** 2 + (end_position[1] - tmp_y_2) ** 2)

        if d_1 < d_2:
            position[0] = tmp_x_1
            position[1] = tmp_y_1
        else:
            position[0] = tmp_x_2
            position[1] = tmp_y_2

        # Turn the tides if we end up outside the boundaries.
        if not 0 + 50 < position[0] < boundaries[0] - 50:
            end_position = position  # force new end point generation.
            propability[0] = 1 - propability[0]  # TODO find end point inside the boundaries.

        if not 0 + 50 < position[1] < boundaries[1] - 50:
            end_position = position
            propability[1] = 1 - propability[1]

    # Random change of propabilities.
    if random.random() > 0.99:
        propability = [random.random(), random.random()]

    # Return the calculated stuff.
    help_array = [end_position[0], end_position[1], position[0], position[1], distance, propability[0], propability[1],
                  lay_egg]

    return help_array, right


def game_start():
    try:
        # Check if sound and font are supported
        if not pygame.font:
            print("Warning, fonts disabled")
        if not pygame.mixer:
            print("Warning, sound disabled")

        # Constants
        background_color = (0, 162, 241)  # Color of the underground
        pathtotextures = os.path.dirname(os.path.realpath(__file__)) + "/textures/"  # path to the textures
        velocity = 300  # Pixels per second.
        step_size = 200  # Step size of each move in pixel.

        # Initiale values.
        propability = [random.random(), random.random()]
        distance = 0
        right = True
        lay_egg = False

        # Initialize Pygame, the clock (for FPS), and a simple counter
        pygame.init()

        # Initialize the display function from Pygame.
        pygame.display.init()
        info = pygame.display.Info()

        # Prints the info about the main screen resolution.
        # print info

        # That info can be used to create a full screen:
        # window_width = 300
        # window_height = 200

        window_width = info.current_w
        window_height = info.current_h

        boundaries = [window_width, window_height]

        # screen = pygame.display.set_mode((window_width, window_height))
        screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN, 32)
        pygame.display.set_caption('Das lustige Huehnchen')

        # Load the textures
        shrink_value_chicken = int(math.floor(0.00007 * window_width * window_height))

        crlcm = pygame.image.load(pathtotextures + "chicken_right_left_closemouth.png")
        crlcm = pygame.transform.smoothscale(crlcm, (shrink_value_chicken, shrink_value_chicken))

        cllcm = pygame.image.load(pathtotextures + "chicken_left_left_closemouth.png")
        cllcm = pygame.transform.smoothscale(cllcm, (shrink_value_chicken, shrink_value_chicken))

        cls = pygame.image.load(pathtotextures + "chicken_left_scream.png")
        cls = pygame.transform.smoothscale(cls, (shrink_value_chicken, shrink_value_chicken))

        crs = pygame.image.load(pathtotextures + "chicken_right_scream.png")
        crs = pygame.transform.smoothscale(crs, (shrink_value_chicken, shrink_value_chicken))

        # Draw the background.
        screen.fill(background_color)

        pygame.display.flip()

        # Draw the text with the background of the text field.
        game_font = pygame.font.SysFont("comicsansms", info.current_w * info.current_h / 20000)
        egg_counter_text = game_font.render("000", True, (143, 215, 244))
        text_width, text_height = game_font.size("000")

        pygame.draw.ellipse(screen, (0, 120, 163),
                            (window_width - 2.25 * text_width, 0.75 * text_height, 1.5 * text_width, 1.5 * text_height),
                            0)

        position = [window_width/2, window_height/2]
        end_position = position

        screen.blit(crlcm, (position[0] - shrink_value_chicken / 2, position[1] - shrink_value_chicken / 2))

        screen.blit(egg_counter_text, (window_width - 2 * text_width, text_height))

        pygame.display.update()

        clock = time.clock()
        egg_counter = 0

        # Endless loop:
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        lay_egg = True
                        egg_counter = egg_counter + 1

            # Calculate the new position of the chicken.
            time_step = time.clock() - clock

            help_array, right = calc_position(end_position, position, distance, velocity, time_step, boundaries,
                                              step_size, propability, right, lay_egg)

            # Translate the help array.
            end_position = [help_array[0], help_array[1]]
            position = [help_array[2], help_array[3]]
            distance = help_array[4]
            propability = [help_array[5], help_array[6]]
            lay_egg = help_array[7]

            # Start new time measurement.
            clock = time.clock()

            # Redraw the background.
            screen.fill(background_color)

            # Draw the chicken.
            if lay_egg:
                if right:
                    screen.blit(cls, ((position[0] - shrink_value_chicken / 2),
                                      (position[1] - shrink_value_chicken / 2)))
                else:
                    screen.blit(crs, ((position[0] - shrink_value_chicken / 2),
                                      (position[1] - shrink_value_chicken / 2)))
            else:
                if right:
                    screen.blit(crlcm, ((position[0] - shrink_value_chicken / 2),
                                        (position[1] - shrink_value_chicken / 2)))
                else:
                    screen.blit(cllcm, ((position[0] - shrink_value_chicken / 2),
                                        (position[1] - shrink_value_chicken / 2)))

            # Draw the eggs
            # TODO

            # Draw the counter stuff again.
            if egg_counter < 10:
                text_string = "00" + str(egg_counter)
            elif egg_counter < 100:
                text_string = "0" + str(egg_counter)
            elif egg_counter < 1000:
                text_string = str(egg_counter)
            else:
                egg_counter = 0
                text_string = "000"

            egg_counter_text = game_font.render(text_string, True, (143, 215, 244))
            text_width, text_height = game_font.size(text_string)

            pygame.draw.ellipse(screen, (0, 120, 163),
                                (window_width - 2.25 * text_width, 0.75 * text_height, 1.5 * text_width,
                                 1.5 * text_height), 0)

            screen.blit(egg_counter_text, (window_width - 2 * text_width, text_height))

            pygame.display.update()

            time.sleep(0.01)

        print("Spiel wird beendet... Ciao!")

    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":

    print("\n\n###################################################")
    print("Spielstart von 'Das lustige Huehnchen'!")
    print("###################################################\n\n")

    game_start()

    sys.exit(0)
