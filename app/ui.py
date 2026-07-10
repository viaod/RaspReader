from pathlib import Path

from app.screen import Screen
from app.screens import HomeScreen


class UI:
    def __init__(self, display=None, assets_dir=None):
        self.display = display
        self.assets_dir = Path(assets_dir or Path(__file__).resolve().parent.parent / "assets")
        self.current_screen = None

    def show_home(self, menu=None):
        if self.display is None:
            return

        self.current_screen = HomeScreen(self.display, self.assets_dir)
        self.current_screen.show()
