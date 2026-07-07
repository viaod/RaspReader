from display import Display
# from encoder import Encoder

from screens.home import HomeScreen
from screens.menu import MenuScreen

import time


def main():

    # Initialise hardware
    display = Display()

    # Encoder disabled while testing display
    # encoder = Encoder()
    # encoder.initialise()

    # Create screens
    home = HomeScreen(display)
    menu = MenuScreen(display)

    # Start on home screen
    current_screen = home
    current_screen.show()

    try:

        while True:

            # Encoder disabled
            #
            # encoder.update()

            # rotation = encoder.get_rotation()
            #
            # if rotation == 1:
            #     current_screen.handle_input("clockwise")
            #
            # elif rotation == -1:
            #     current_screen.handle_input("counter_clockwise")


            # Buttons disabled
            #
            # button = encoder.button_pressed()
            #
            # if button == "select":
            #
            #     if current_screen == home:
            #         current_screen = menu
            #         current_screen.draw()
            #
            #     else:
            #         current_screen.handle_input("select")
            #
            # elif button:
            #
            #     current_screen.handle_input(button)


            time.sleep(0.02)

    except KeyboardInterrupt:

        display.sleep()


if __name__ == "__main__":
    main()