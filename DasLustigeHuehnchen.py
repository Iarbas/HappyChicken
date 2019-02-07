#!/usr/bin/python

# Das folgende Programm ist ein Spiel, welches von Peppa Wutz stammt und den Namen traegt "Das lustige Huehnchen".
#
# Autor:  Andre Alexander Pieper.
# Version 1.0
# Datum:  03.02.2019
# Lizenz: LGPLv3

import os
import sys
import traceback
import time
import math
import random
import copy
import pygame


def find_point_between_two_points(start_point, end_point, distance):
    position = [0, 0]

    m = (start_point[1] - end_point[1]) / (start_point[0] - end_point[0])
    n = end_point[1] - end_point[0] * m

    p = (2 * m * n - 2 * start_point[0] - 2 * m * start_point[1]) / (1 + m ** 2)
    q = (start_point[0] ** 2 + n ** 2 - 2 * n * start_point[1] + start_point[1] ** 2 - distance ** 2) / (1 + m ** 2)

    tmp_x_1 = - p / 2 + math.sqrt((p / 2) ** 2 - q)
    tmp_x_2 = - p / 2 - math.sqrt((p / 2) ** 2 - q)

    tmp_y_1 = m * tmp_x_1 + n
    tmp_y_2 = m * tmp_x_2 + n

    d_1 = math.sqrt((end_point[0] - tmp_x_1) ** 2 + (end_point[1] - tmp_y_1) ** 2)
    d_2 = math.sqrt((end_point[0] - tmp_x_2) ** 2 + (end_point[1] - tmp_y_2) ** 2)

    if d_1 < d_2:
        position[0] = tmp_x_1
        position[1] = tmp_y_1
    else:
        position[0] = tmp_x_2
        position[1] = tmp_y_2

    return position


def calc_position(end_position, old_position, distance_old, velocity, time_step, boundaries, step_size, right):

    position = copy.deepcopy(old_position)
    distance = math.sqrt((end_position[0] - old_position[0]) ** 2 + (end_position[1] - old_position[1]) ** 2)
    end_position_tmp = [0, 0]
    change = False

    # Check, if the chicken runs over an end point.
    if right and end_position[0] <= old_position[0]:
        change = True
    elif not right and end_position[0] >= old_position[0]:
        change = True

    # Generation of a new end point, if we come close to the old end point or step over.
    if change:

        # First and second loop condition.
        iteration = 0
        distance_pos2new_pos = 0

        # Find a new point in the boundaries:
        while iteration < 10 and distance_pos2new_pos < step_size[0]:
            iteration = iteration + 1

            end_position_tmp = [random.random() * boundaries[0], random.random() * boundaries[1]]

            # Define a point between actual position and the random (temporary) end position.
            distance_pos2new_pos = math.sqrt((end_position_tmp[0] - old_position[0]) ** 2 +
                                             (end_position_tmp[1] - old_position[1]) ** 2)

        # If the distance is higher than the allowed step size,
        if distance_pos2new_pos > step_size[1]:
            # Find a new end point along the path.
            end_position = find_point_between_two_points(old_position, end_position_tmp,
                                                         step_size[0] + random.random() * (step_size[1] - step_size[0]))
        else:
            end_position = end_position_tmp

        distance = math.sqrt((end_position[0] - old_position[0]) ** 2 + (end_position[1] - old_position[1]) ** 2)

        # Determine the move direction.
        if end_position[0] - old_position[0] > 0:
            right = True
        else:
            right = False

    # Or go further.
    else:
        d = velocity * time_step
        position = find_point_between_two_points(old_position, end_position, d)

    # Return the calculated stuff.
    help_array = [end_position[0], end_position[1], position[0], position[1], distance]

    return help_array, right


def calc_jump(position, jump_height, refreshed_time, time_of_laying, egg_laying_time):

    # Set the jump to the original position.
    jump_position = copy.deepcopy(position)

    # Calculate the time difference.
    time_diff = refreshed_time - time_of_laying

    if time_diff > egg_laying_time:
        time_diff = egg_laying_time

    # ---- Calculate new y coordinate. ----
    # Get the percentage of the passed time to the time of laying an egg.
    percentage = time_diff / egg_laying_time

    # The jump has two parts, at first the jump to the max. height at the half of the egg laying time and afterwards the
    # fall back.
    if time_diff <= (egg_laying_time / 2):
        jump_position[1] = position[1] - 2 * percentage * jump_height
    else:
        jump_position[1] = position[1] - 2 * (1 - percentage) * jump_height

    return jump_position


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
        pathtosounds = os.path.dirname(os.path.realpath(__file__)) + "/sounds/"  # path to the sounds
        velocity = 150  # Pixels per second.
        step_size = [200, 600]  # Min and max step size of each move in pixel.
        egg_laying_time = 0.5  # time in which the chicken lays the egg (in seconds)

        # Initial values.
        distance = 0
        right = True
        lay_egg = False
        time_of_laying = 0
        egg_counter = 0
        list_eggs = []

        # Initialize Pygame, the clock (for FPS), the background music and a simple counter
        pygame.init()
        refreshed_time = time.time()
        pygame.mixer.music.load(pathtosounds + 'Background_Music.mp3')
        pygame.mixer.music.play(-1)
        screams = [pygame.mixer.Sound(pathtosounds + 'Scream1.wav'), pygame.mixer.Sound(pathtosounds + 'Scream2.wav'),
                   pygame.mixer.Sound(pathtosounds + 'Scream3.wav'), pygame.mixer.Sound(pathtosounds + 'Scream4.wav'),
                   pygame.mixer.Sound(pathtosounds + 'Scream5.wav'), pygame.mixer.Sound(pathtosounds + 'Scream6.wav'),
                   pygame.mixer.Sound(pathtosounds + 'Scream7.wav')]

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

        # Initial calculation of the position and borders.
        position = [window_width/2, window_height/2]
        end_position = position
        jump_position = position

        # screen = pygame.display.set_mode((window_width, window_height))
        screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN, 32)
        pygame.display.set_caption('Das lustige Huehnchen')

        # Load the textures
        shrink_value_chicken = int(math.floor(0.00007 * window_width * window_height))

        # Load the chicken textures.
        crlcm = pygame.image.load(pathtotextures + "chicken_right_left_closemouth.png")
        crlcm = pygame.transform.smoothscale(crlcm, (shrink_value_chicken, shrink_value_chicken))

        cllcm = pygame.image.load(pathtotextures + "chicken_left_left_closemouth.png")
        cllcm = pygame.transform.smoothscale(cllcm, (shrink_value_chicken, shrink_value_chicken))

        cls = pygame.image.load(pathtotextures + "chicken_left_scream.png")
        cls = pygame.transform.smoothscale(cls, (shrink_value_chicken, shrink_value_chicken))

        crs = pygame.image.load(pathtotextures + "chicken_right_scream.png")
        crs = pygame.transform.smoothscale(crs, (shrink_value_chicken, shrink_value_chicken))

        size_chicken_image = crs.get_rect().size

        # Load the egg textures and calculate the jump height.
        shrink_value_egg = int(math.floor(0.00003 * window_width * window_height))

        egg1 = pygame.image.load(pathtotextures + "egg_1.png")
        egg1 = pygame.transform.smoothscale(egg1, (shrink_value_egg, shrink_value_egg))

        egg2 = pygame.image.load(pathtotextures + "egg_2.png")
        egg2 = pygame.transform.smoothscale(egg2, (shrink_value_egg, shrink_value_egg))

        size_egg_image = egg2.get_rect().size

        boundaries = [window_width - size_chicken_image[0], window_height - size_chicken_image[1]]
        jump_height = copy.deepcopy(shrink_value_egg)  # jump height is the size of the eggs

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

        screen.blit(crlcm, (position[0] - shrink_value_chicken / 2, position[1] - shrink_value_chicken / 2))

        screen.blit(egg_counter_text, (window_width - 2 * text_width, text_height))

        pygame.display.update()

        # Endless loop:
        running = True

        while running:

            # Get time.
            old_time = refreshed_time
            refreshed_time = time.time()

            # Check the system clock, if it wasn't manipulated at runtime.
            if refreshed_time < old_time or refreshed_time < time_of_laying:
                print("Corrupted system clock. The game can't continue!")
                running = False

            # Handle the keyboard input.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE and not lay_egg:
                        lay_egg = True
                        time_of_laying = refreshed_time
                        egg_counter = egg_counter + 1
                        list_eggs.append([position[0] + (size_chicken_image[0] - size_egg_image[0]) / 2,
                                          position[1] + size_chicken_image[1] - 1.3 * size_egg_image[1],
                                          int(round(random.random()))])
                        # Play the chicken scream.
                        screams[int(round(6 * random.random()))].play()

            # ---- Calculate the new position of the chicken. ----
            # Get the passed time since the last iteration and afterwards save the actual time.
            time_step = refreshed_time - old_time

            # Get the new position
            # If a egg is been laid, we need to jump. Otherwise we follow our path.
            if lay_egg:
                jump_position = calc_jump(position, jump_height, refreshed_time, time_of_laying, egg_laying_time)

                # Set the flag back, after the egg was laid.
                if refreshed_time - time_of_laying >= egg_laying_time:
                    lay_egg = False
            else:
                help_array, right = calc_position(end_position, position, distance, velocity, time_step, boundaries,
                                                  step_size, right)

                # Translate the help array.
                end_position = [help_array[0], help_array[1]]
                position = [help_array[2], help_array[3]]
                distance = help_array[4]

            # ---- Draw everything anew. ----
            # Redraw the background.
            screen.fill(background_color)

            # Draw the eggs
            for egg_item in list_eggs:
                if egg_item[2] == 0:
                    screen.blit(egg1, ((egg_item[0] - shrink_value_chicken / 2),
                                       (egg_item[1] - shrink_value_chicken / 2)))
                else:
                    screen.blit(egg2, ((egg_item[0] - shrink_value_chicken / 2),
                                       (egg_item[1] - shrink_value_chicken / 2)))

            # Draw the chicken.
            if lay_egg:
                if right:
                    screen.blit(crs, ((jump_position[0] - shrink_value_chicken / 2),
                                      (jump_position[1] - shrink_value_chicken / 2)))
                else:
                    screen.blit(cls, ((jump_position[0] - shrink_value_chicken / 2),
                                      (jump_position[1] - shrink_value_chicken / 2)))
            else:
                if right:
                    screen.blit(crlcm, ((position[0] - shrink_value_chicken / 2),
                                        (position[1] - shrink_value_chicken / 2)))
                else:
                    screen.blit(cllcm, ((position[0] - shrink_value_chicken / 2),
                                        (position[1] - shrink_value_chicken / 2)))

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
        pygame.mixer.music.stop()
        print("Shutdown requested...exiting")
    except Exception:
        pygame.mixer.music.stop()
        traceback.print_exc(file=sys.stdout)

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":

    print("\n\n###################################################")
    print("Spielstart von 'Das lustige Huehnchen'!")
    print("###################################################\n\n")

    game_start()

    sys.exit(0)
