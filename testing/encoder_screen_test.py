import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

from display import Display
from encoder import Encoder


class FakeScreen:
    def __init__(self, name, display):
        self.name = name
        self.display = display

    def show(self):
        print(f"Showing {self.name}")

    def handle_input(self, event):
        print(f"{self.name} received: {event}")


class ScreenController:
    def __init__(self, screens):
        self.screens = screens
        self.current = 0

    def handle_event(self, event):
        if event == "clockwise":
            self.current = (self.current + 1) % len(self.screens)
            self.screens[self.current].show()
        elif event == "counter_clockwise":
            self.current = (self.current - 1) % len(self.screens)
            self.screens[self.current].show()
        elif event in {"select", "left", "right"}:
            self.screens[self.current].handle_input(event)


def main():
    display = Display()
    encoder = Encoder()
    encoder.initialise()

    screens = [
        FakeScreen("Screen 1", display),
        FakeScreen("Screen 2", display),
        FakeScreen("Screen 3", display),
    ]
    controller = ScreenController(screens)
    encoder.add_listener(controller.handle_event)

    screens[0].show()

    try:
        while True:
            encoder.update()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        display.sleep()


if __name__ == "__main__":
    main()
