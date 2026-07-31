

class Screen:
    def __init__(self, display, assets_dir=None, ui=None):
        self.display = display
        self.ui = ui
        self.assets_dir = Path(
            assets_dir or Path(__file__).resolve().parent.parent.parent / "assets"
        )

    def show(self):
        raise NotImplementedError

    def handle_input(self, event):
        """Override in subclasses if the screen reacts to input."""
        pass