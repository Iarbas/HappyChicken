#!/usr/bin/python

# Das folgende Programm ist ein Spiel, welches von Peppa Wutz stammt und den Namen traegt "Das lustige Huehnchen".
#
# Autor:  Andre Alexander Pieper.
# Version 1.0
# Datum:  01.02.2018
# Lizenz: LGPLv3

import sys, traceback, time
import pygame


def game_start():
    try:
        # Check if sound and font are supported
        if not pygame.font:
            print "Warning, fonts disabled"
        if not pygame.mixer:
            print "Warning, sound disabled"

        # Constants
        background_color = (0, 162, 241)

        # Initialize Pygame, the clock (for FPS), and a simple counter
        pygame.init()

        # Initialize the display function from Pygame.
        pygame.display.init()
        info = pygame.display.Info()

        # Prints the info about the main screen resolution.
        # print info

        # The info can be used to create a full screen:
        screen = pygame.display.set_mode((300, 200))
        # screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN, 32)
        pygame.display.set_caption('Das lustige Huehnchen')

        # Draw the background.
        screen.fill(background_color)

        pygame.display.flip()

        # Draw the text with the background of the text field.
        game_font = pygame.font.SysFont("comicsansms", info.current_w * info.current_h / 20000)
        egg_counter_text = game_font.render("000", True, (143, 215, 244))
        text_width, text_height = game_font.size("000")

        pygame.draw.ellipse(screen, (0, 120, 163),
                            (300 - 2.25 * text_width, 0.75 * text_height, 1.5 * text_width, 1.5 * text_height), 0)

        screen.blit(egg_counter_text, (300 - 2 * text_width, text_height))

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
                                (300 - 2.25 * text_width, 0.75 * text_height, 1.5 * text_width, 1.5 * text_height), 0)

            screen.blit(egg_counter_text, (300 - 2 * text_width, text_height))

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
