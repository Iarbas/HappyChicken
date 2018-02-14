#!/usr/bin/python

# Das folgende Programm ist ein Spiel, welches von Peppa Wutz stammt und den Namen traegt "Das lustige Huehnchen".
#
# Autor:  Andre Alexander Pieper.
# Version 1.0
# Datum:  01.02.2018
# Lizenz: LGPLv3

import os, sys, traceback, time, math
import pygame


def game_start():
    try:
        # Check if sound and font are supported
        if not pygame.font:
            print "Warning, fonts disabled"
        if not pygame.mixer:
            print "Warning, sound disabled"

        # Constants
        background_color = (0, 162, 241)  # Color of the underground
        pathtotextures = os.path.dirname(os.path.realpath(__file__)) + "/textures/"  # path to the textures

        # Initialize Pygame, the clock (for FPS), and a simple counter
        pygame.init()

        # Initialize the display function from Pygame.
        pygame.display.init()
        info = pygame.display.Info()

        # Prints the info about the main screen resolution.
        # print info

        # The info can be used to create a full screen:
        # window_width = 300
        # window_height = 200

        window_width = info.current_w
        window_height = info.current_h

        print window_width
        print window_height

        # screen = pygame.display.set_mode((window_width, window_height))
        screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN, 32)
        pygame.display.set_caption('Das lustige Huehnchen')

        # Load the textures
        shrink_value_chicken = int(math.floor(0.00007 * window_width * window_height))

        crlcm = pygame.image.load(pathtotextures + "chicken_right_left_closemouth.png")
        crlcm = pygame.transform.smoothscale(crlcm, (shrink_value_chicken, shrink_value_chicken))

        # Draw the background.
        screen.fill(background_color)

        pygame.display.flip()

        # Draw the text with the background of the text field.
        game_font = pygame.font.SysFont("comicsansms", info.current_w * info.current_h / 20000)
        egg_counter_text = game_font.render("000", True, (143, 215, 244))
        text_width, text_height = game_font.size("000")

        pygame.draw.ellipse(screen, (0, 120, 163),
                            (window_width - 2.25 * text_width, 0.75 * text_height, 1.5 * text_width, 1.5 * text_height), 0)

        screen.blit(crlcm, (window_width/2 - shrink_value_chicken, window_height/2 - shrink_value_chicken))

        screen.blit(egg_counter_text, (window_width - 2 * text_width, text_height))

        pygame.display.update()

        clock = pygame.time.Clock()
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
                        egg_counter = egg_counter + 1

            # Redraw the background.
            screen.fill(background_color)

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

            screen.blit(crlcm, ((window_width - shrink_value_chicken) / 2, (window_height - shrink_value_chicken) / 2))

            screen.blit(egg_counter_text, (window_width - 2 * text_width, text_height))

            pygame.display.update()

            time.sleep(0.01)

        print "Spiel wird beendet... Ciao!"

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":

    print "\n\n###################################################"
    print "Spielstart von 'Das lustige Huehnchen'!"
    print "###################################################\n\n"

    game_start()

    sys.exit(0)