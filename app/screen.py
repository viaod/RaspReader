from pathlib import Path

class Screen:

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        **services
    ):
        self.display = display
        self.assets_dir = assets_dir
        self.ui = ui

        for name, value in services.items():
            setattr(self, name, value)

    def show(self):
        raise NotImplementedError

    def handle_input(self, event):
        """Override in subclasses if the screen reacts to input."""
        pass