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

        bbox = self.display.draw.textbbox((0, 0), "Upload", font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (self.display.height - text_width) // 2
        self.display.draw.text(
            (x, 25),
            "Upload",
            font=font_title,
            fill=0,
        )

        for y, text in [
            (60, "Please upload a book via the web interface."),
            (100, f"URL: http://{self.get_ip()}:8080"),
        ]:
            bbox = self.display.draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.display.height - text_width) // 2
            self.display.draw.text(
                (x, y),
                text,
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