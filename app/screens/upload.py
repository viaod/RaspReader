import subprocess

from app.core.events import Event
from app.screen import Screen
from app.core.config import FONT_SIZE_SCREEN_BODY, FONT_SIZE_SCREEN_TITLE


class UploadScreen(Screen):

    def show(self):

        self.app.web_server.start()

        self.display.clear_image()
        self.draw_status_header()

        font_title = self.display.get_font(FONT_SIZE_SCREEN_TITLE)
        font = self.display.get_font(FONT_SIZE_SCREEN_BODY)

        self.display.draw.text(
            (20, 20),
            "Upload",
            font=font_title,
            fill=0,
        )

        self.display.draw.text(
            (20, 60),
            "Please upload a book via the web interface.",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 100),
            f"URL: http://{self.get_ip()}:8080",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 220),
            "< Left to return",
            font=font,
            fill=0,
        )

        self.display.refresh()


    def handle_input(self, event):

        if event == Event.LEFT:

            self.app.web_server.stop()

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