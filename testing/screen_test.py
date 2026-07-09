import os
import select
import sys
import time
from pathlib import Path

# Resolve the project root from this script's location so the tests work
# even when launched from another directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import msvcrt
except ImportError:  # pragma: no cover - non-Windows
    msvcrt = None

from display import Display

from screens.home import HomeScreen
from screens.menu import MenuScreen
from screens.reader_menu import ReaderMenuScreen
from screens.library import LibraryScreen
from screens.reader import ReaderScreen
from screens.settings import SettingsScreen
from screens.upload import UploadScreen


def _read_keyboard_command():
    if os.name == "nt" and msvcrt is not None:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key in {"\x03", "q", "Q"}:
                raise KeyboardInterrupt
            return key.lower()
        return None

    if select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1)
        if key in {"\x03", "q", "Q"}:
            raise KeyboardInterrupt
        return key.lower()

    return None


def test():
    display = Display()

    try:
        from encoder import Encoder
    except Exception as exc:  # pragma: no cover - hardware-dependent
        print(f"Encoder not available: {exc}")
        encoder = None
    else:
        try:
            encoder = Encoder()
            encoder.initialise()
            print("Encoder ready")
        except Exception as exc:  # pragma: no cover - hardware-dependent
            print(f"Encoder initialization failed: {exc}")
            encoder = None

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
            screen.show()

            print("\nCommands:")
            print("  n = next screen")
            print("  p = previous screen")
            print("  q = quit")
            print("  l = left")
            print("  r = right")
            print("  s = select")
            print("  encoder movement/button will also be handled when available")

            while True:
                if encoder is not None:
                    encoder.update()

                    rotation = encoder.get_rotation()
                    if rotation > 0:
                        if hasattr(screen, "handle_input"):
                            screen.handle_input("clockwise")
                            screen.show()
                        time.sleep(0.15)
                        break

                    if rotation < 0:
                        if hasattr(screen, "handle_input"):
                            screen.handle_input("counter_clockwise")
                            screen.show()
                        time.sleep(0.15)
                        break

                    button = encoder.button_pressed()
                    if button is not None:
                        if hasattr(screen, "handle_input"):
                            mapped = button
                            if button in {"up", "down"}:
                                mapped = "clockwise" if button == "down" else "counter_clockwise"
                            elif button == "select":
                                mapped = "select"
                            elif button == "left":
                                mapped = "left"
                            elif button == "right":
                                mapped = "right"

                            result = screen.handle_input(mapped)
                            screen.show()
                            if result is not None:
                                print(f"Selected: {result}")
                        time.sleep(0.15)
                        break

                command = _read_keyboard_command()
                if command is None:
                    time.sleep(0.05)
                    continue

                if command == "n":
                    current = (current + 1) % len(screens)
                    break

                if command == "p":
                    current = (current - 1) % len(screens)
                    break

                if command in {"q", "\x03"}:
                    raise KeyboardInterrupt

                if command in {"l", "left"}:
                    if hasattr(screen, "handle_input"):
                        screen.handle_input("left")
                        screen.show()
                    continue

                if command in {"r", "right"}:
                    if hasattr(screen, "handle_input"):
                        screen.handle_input("right")
                        screen.show()
                    continue

                if command in {"s", "select"}:
                    if hasattr(screen, "handle_input"):
                        result = screen.handle_input("select")
                        screen.show()
                        print(f"Selected: {result}")
                    continue

    except KeyboardInterrupt:
        pass

    finally:
        display.sleep()


if __name__ == "__main__":
    test()