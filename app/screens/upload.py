import subprocess

from app.core.events import Event
from app.screen import Screen
from app.web.server import WebServer


class UploadScreen(Screen):

    def show(self):
        self.server = WebServer()
        self.server.start()

        self.display.clear_image()

        font_title = self.display.get_font(22)
        font = self.display.get_font(18)

        # Title
        self.display.draw.text(
            (20, 20),
            "Upload",
            font=font_title,
            fill=0,
        )

        # Instructions
        self.display.draw.text(
            (20, 60),
            "Please upload a book via the web interface.",
            font=font,
            fill=0,
        )

        # Web server URL
        self.display.draw.text(
            (20, 100),
            f"URL: http://{self.get_ip()}:8080",
            font=font,
            fill=0,
        )

        # Back hint
        self.display.draw.text(
            (20, 220),
            "< Left to return",
            font=font,
            fill=0,
        )

        self.display.refresh()

    def handle_input(self, event):
        if event == Event.LEFT:
            self.server.stop()

            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)
            
    def get_ip(self):

        try:

            ip = subprocess.check_output(
                ["hostname", "-I"],
                text=True,
            ).split()

            if ip:
                return ip[0]

        except Exception:
            pass

        return "No IP"