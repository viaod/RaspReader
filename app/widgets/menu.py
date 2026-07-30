from dataclasses import dataclass
import subprocess

from PIL import ImageFont

from app.core.events import Event
from app.screen import Screen


@dataclass
class MenuItem:
    text: str
    action: callable = None
    screen: type = None


class MenuScreen(Screen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        title="Menu",
        items=None,
    ):
        super().__init__(display, assets_dir, ui)

        self.title = title
        self.items = items or []
        self.selected = 0

        self.title_font = ImageFont.load_default()
        self.item_font = ImageFont.load_default()

    def show(self):

        self.display.clear_image()

        draw = self.display.draw

        draw.text(
            (20, 20),
            self.title,
            font=self.display.get_font(24),
            fill=0,
        )
        
        draw.line((15, 38, 400, 38), fill=0)

        y = 60

        for i, item in enumerate(self.items):

            prefix = "▶ " if i == self.selected else "  "

            draw.text(
                (20, y),
                prefix + item.text,
                font=self.display.get_font(20),
                fill=0,
            )

            y += 25
            
        #
        # Footer
        #

        wifi = self.get_wifi_status()
        ip = self.get_ip()

        draw.line((0, 215, 415, 215), fill=0)

        draw.text(
            (10, 222),
            wifi,
            font=self.display.get_font(18),
            fill=0,
        )
        
        w = draw.textlength(ip, font=self.display.get_font(18))

        draw.text(
            (415 - w - 10, 222),
            ip,
            font=self.display.get_font(18),
            fill=0,
        )

        self.display.refresh()

    def handle_input(self, event):

        if event == Event.DOWN:

            self.selected = (self.selected + 1) % len(self.items)
            self.show()

        elif event == Event.UP:

            self.selected = (self.selected - 1) % len(self.items)
            self.show()

        elif event == Event.SELECT:

            item = self.items[self.selected]

            if item.screen is not None:
                self.ui.show(item.screen)

            elif item.action is not None:
                item.action()

        elif event == Event.LEFT:

            self.back()

    def back(self):
        pass
    
    def get_wifi_status(self):

        try:

            result = subprocess.check_output(
                ["cat", "/sys/class/net/wlan0/operstate"],
                text=True,
            ).strip()

            if result == "up":
                return "WiFi [ ON ]"

            return "WiFi [ OFF ]"

        except Exception:

            return "WiFi ?"

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
    