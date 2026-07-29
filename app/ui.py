from pathlib import Path

from app.screens.home import HomeScreen


class UI:
    def __init__(self, display=None, assets_dir=None):
        self.display = display
        self.assets_dir = Path(
            assets_dir or Path(__file__).resolve().parent.parent / "assets"
        )

        self.current_screen = None

    def show(self, screen_cls):

        if self.display is None:
            return

        self.current_screen = screen_cls(
            self.display,
            self.assets_dir,
            self,
        )

        self.current_screen.show()

    def handle_input(self, event):
        if self.current_screen is not None:
            self.current_screen.handle_input(event)