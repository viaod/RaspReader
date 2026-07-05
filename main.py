from display import Display
from screens.home import HomeScreen


def main():

    display = Display()

    current_screen = HomeScreen(display)

    current_screen.show()

    input("Press Enter to quit...")

    display.sleep()


if __name__ == "__main__":
    main()