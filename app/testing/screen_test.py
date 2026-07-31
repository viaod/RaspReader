#!/usr/bin/env python3

from app.hardware.display import Display
from app.core.ui import UI

# Import the screen you want to test
# from app.screens.storage import StorageScreen
# from app.screens.settings_menu import SettingsScreen
# from app.screens.shutdown import ShutdownScreen
# from app.screens.main_menu import MainMenu
# from app.screens.home import HomeScreen

from app.screens.upload import UploadScreen


def main():
    display = Display()
    ui = UI(display)

    ui.show(UploadScreen)

    print("Displaying screen. Press Ctrl+C to exit.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        display.clear_image()
        display.refresh()
        display.sleep()


if __name__ == "__main__":
    main()