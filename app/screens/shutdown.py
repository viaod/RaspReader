import subprocess

from app.core.events import Event
from app.screen import Screen


class ShutdownScreen(Screen):

    def show(self):

        self.display.clear_image()

        title_font = self.display.get_font(22)
        font = self.display.get_font(18)

        self.display.draw.text(
            (20, 20),
            "Shutdown?",
            font=title_font,
            fill=0,
        )

        self.display.draw.text(
            (20, 70),
            "Press SELECT",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 95),
            "to power off.",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 170),
            "LEFT = Cancel",
            font=font,
            fill=0,
        )

        self.display.refresh()

    def handle_input(self, event):

        if event == Event.LEFT:
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)

        elif event == Event.SELECT:
            self.power_off()

    def power_off(self):

        self.display.clear_image()

        font = self.display.get_font(22)

        self.display.draw.text(
            (20, 100),
            "Shutting down...",
            font=font,
            fill=0,
        )

        self.display.refresh()

        subprocess.run(
            ["sudo", "shutdown", "-h", "now"],
            check=False,
        )