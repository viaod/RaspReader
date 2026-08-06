from datetime import datetime
from pathlib import Path

class Screen:

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        app=None,
    ):
        self.display = display
        self.assets_dir = assets_dir
        self.ui = ui
        self.app = app

    def show(self):
        raise NotImplementedError

    def draw_status_header(self):
        """Draw the shared status information at the top of the display."""
        font = self.display.get_font(14)
        time_text = datetime.now().strftime("%H:%M")
        battery_text = "100%"

        self.display.draw.text((10, 4), time_text, font=font, fill=0)
        battery_width = self.display.draw.textlength(battery_text, font=font)
        self.display.draw.text(
            (self.display.height - battery_width - 10, 4),
            battery_text,
            font=font,
            fill=0,
        )

    def handle_input(self, event):
        """Override in subclasses if the screen reacts to input."""
        pass