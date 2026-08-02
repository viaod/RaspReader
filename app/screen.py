from pathlib import Path

class Screen:

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        app=None,
        book_reader=None,

    ):
        self.display = display
        self.assets_dir = assets_dir
        self.ui = ui
        self.app = app
        self.book_reader = book_reader

    def show(self):
        raise NotImplementedError

    def handle_input(self, event):
        """Override in subclasses if the screen reacts to input."""
        pass