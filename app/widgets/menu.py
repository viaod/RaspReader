from dataclasses import dataclass
import subprocess

from PIL import ImageFont

from app.core.events import Event
from app.screen import Screen
from app.core.config import FONT_SIZE_MENU_FOOTER, FONT_SIZE_MENU_ITEM, FONT_SIZE_MENU_TITLE


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
        app=None,
    ):
        super().__init__(
            display,
            assets_dir,
            ui,
            app=app,
        )

        self.app = app
        
        self.title = title
        self.items = items or []

        self.selected = 0
        self.scroll_offset = 0

        self.item_height = 25
        self.menu_start_y = 60

        self.title_font = ImageFont.load_default()
        self.item_font = ImageFont.load_default()

        # Calculate how many items fit
        footer_height = 40
        available_height = self.display.width - self.menu_start_y - footer_height

        self.visible_items = max(1, (available_height // self.item_height) + 1)

    def show(self):

        self.display.clear_image()
        self.draw_status_header()

        draw = self.display.draw

        #
        # Title
        #

        draw.text(
            (20, 20),
            self.title,
            font=self.display.get_font(FONT_SIZE_MENU_TITLE),
            fill=0,
        )

        draw.line(
            (15, 45, self.display.height - 15, 45),
            fill=0,
        )

        #
        # Menu items
        #

        start = self.scroll_offset
        end = min(start + self.visible_items, len(self.items))

        y = self.menu_start_y

        for i in range(start, end):

            item = self.items[i]

            prefix = "▶ " if i == self.selected else "  "

            draw.text(
                (20, y),
                prefix + item.text,
                font=self.display.get_font(FONT_SIZE_MENU_ITEM),
                fill=0,
            )

            y += self.item_height

        #
        # Scroll indicator
        #

        if len(self.items) > self.visible_items:

            scrollbar_height = int((self.visible_items / len(self.items)) * 100)

            scrollbar_height = max(scrollbar_height, 10)

            max_scroll = len(self.items) - self.visible_items

            if max_scroll > 0:
                scrollbar_y = int(
                    60 + (100 - scrollbar_height) * (self.scroll_offset / max_scroll)
                )

                draw.rectangle(
                    (
                        self.display.height - 8,
                        scrollbar_y,
                        self.display.height - 4,
                        scrollbar_y + scrollbar_height,
                    ),
                    fill=0,
                )

        #
        # Footer
        #

        footer_y = self.display.width - 20

        draw.line(
            (0, footer_y - 5, self.display.height, footer_y - 5),
            fill=0,
        )

        wifi = self.get_wifi_status()
        ip = self.get_ip()

        draw.text(
            (10, footer_y),
            wifi,
            font=self.display.get_font(FONT_SIZE_MENU_FOOTER),
            fill=0,
        )

        ip_width = draw.textlength(ip, font=self.display.get_font(FONT_SIZE_MENU_FOOTER))

        draw.text(
            (self.display.height - ip_width - 10, footer_y),
            ip,
            font=self.display.get_font(FONT_SIZE_MENU_FOOTER),
            fill=0,
        )

        self.display.refresh()

    def handle_input(self, event):

        if not self.items:
            return

        #
        # Move down
        #

        if event == Event.DOWN:

            self.selected = (self.selected + 1) % len(self.items)

            if self.selected == 0:
                # Wrapped to the top
                self.scroll_offset = 0

            elif self.selected >= self.scroll_offset + self.visible_items:
                self.scroll_offset = self.selected - self.visible_items + 1

            self.show()

        #
        # Move up
        #

        elif event == Event.UP:

            self.selected = (self.selected - 1) % len(self.items)

            if self.selected == len(self.items) - 1:
                # Wrapped to the bottom
                self.scroll_offset = max(
                    0,
                    len(self.items) - self.visible_items,
                )

            elif self.selected < self.scroll_offset:
                self.scroll_offset = self.selected

            self.show()

        #
        # Select
        #

        elif event == Event.SELECT:

            item = self.items[self.selected]

            if item.screen is not None:
                self.ui.show(item.screen)

            elif item.action is not None:
                item.action()

        #
        # Back
        #

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
