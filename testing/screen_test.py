import sys
from pathlib import Path

# Add the project root (RaspReader) to Python's path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from display import Display

from screens.home import HomeScreen
from screens.menu import MenuScreen
from screens.reader_menu import ReaderMenuScreen
from screens.library import LibraryScreen
from screens.reader import ReaderScreen
from screens.settings import SettingsScreen
from screens.upload import UploadScreen

import time


def test():

    display = Display()

    # Create screens
    screens = [
        ("Home", HomeScreen(display)),
        ("Menu", MenuScreen(display)),
        ("Reader Menu", ReaderMenuScreen(display)),
        # ("Library", LibraryScreen(display)),
        # ("Reader", ReaderScreen(display)),
        ("Settings", SettingsScreen(display)),
        ("Upload", UploadScreen(display)),
    ]

    current = 0

    try:

        while True:

            name, screen = screens[current]

            print(f"Showing {name} screen")

            # Each screen should implement show()
            screen.show()

            print("\nCommands:")
            print("  n = next screen")
            print("  p = previous screen")
            print("  q = quit")

            command = input("> ")

            if command == "n":
                current += 1
                if current >= len(screens):
                    current = 0

            elif command == "p":
                current -= 1
                if current < 0:
                    current = len(screens) - 1

            elif command == "q":
                break

    except KeyboardInterrupt:
        pass

    finally:
        display.sleep()


if __name__ == "__main__":
    test()