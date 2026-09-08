from dataclasses import dataclass
import subprocess
import textwrap

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
        grid=False,
    ):
        super().__init__(
            display,
            assets_dir,
            ui,
            app=app,
        )

        self.app = app

        self.grid = grid

        self.title = title
        self.items = items or []

        self.selected = 0
        self.scroll_offset = 0
        self.grid_offset = 0
        self._has_rendered = False
        self._last_selected = None
        self._last_scroll_offset = None

        self.item_height = 25
        self.menu_start_y = 70

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

        title_font = self.display.get_font(FONT_SIZE_MENU_TITLE)
        title_bbox = draw.textbbox((0, 0), self.title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]

        x = (self.display.height - title_width) // 2

        draw.text(
            (x, 20),
            self.title,
            font=title_font,
            fill=0,
        )

        draw.line(
            (15, 48, self.display.height - 15, 48),
            fill=0,
        )

        #
        # Menu items
        #

        if self.grid:
            self.grid_format(draw)
        else:
            self.scroll_format(draw)


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

        self.display.refresh_fast()
        self._has_rendered = True
        self._last_selected = self.selected
        self._last_scroll_offset = self.scroll_offset

    def handle_input(self, event):

        if not self.items:
            return

        if self.grid:
            self.handle_grid_input(event)
            return

        #
        # Move down
        #

        if event in (Event.DOWN, Event.ROTATE_RIGHT):

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

        elif event in (Event.UP, Event.ROTATE_LEFT):

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

        # elif event == Event.RIGHT:
        # go to the other side of the grid

        # elif event == Event.LEFT:
        # //

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

    def scroll_format(self, draw):
        start = self.scroll_offset
        end = min(start + self.visible_items, len(self.items))

        y = self.menu_start_y

        for i in range(start, end):

            item = self.items[i]

            item_color = self.display.epd.GRAY3 if item.text == "Back" else 0

            draw.text(
                (20, y),
                ">" if i == self.selected else " ",
                font=self.display.get_font(FONT_SIZE_MENU_ITEM),
                fill=0,
            )

            draw.text(
                (38, y),
                item.text,
                font=self.display.get_font(FONT_SIZE_MENU_ITEM),
                fill=item_color,
            )

            y += self.item_height

        #
        # Scroll indicator
        #

        if len(self.items) > self.visible_items:

            track_top = self.menu_start_y
            track_bottom = self.display.width - 35
            track_height = track_bottom - track_top

            scrollbar_height = max(
                10,
                int(track_height * self.visible_items / len(self.items)),
            )
            scrollbar_height = min(scrollbar_height, track_height)

            max_scroll = len(self.items) - self.visible_items
            scrollbar_y = int(
                track_top
                + (track_height - scrollbar_height)
                * (self.scroll_offset / max_scroll)
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

    def grid_format(self, draw):
        columns = 3
        gap = 10
        grid_left = 15
        grid_right = self.display.height - 15
        grid_top = self.menu_start_y
        grid_bottom = self.display.width - 35
        cell_width = (grid_right - grid_left - gap * (columns - 1)) // columns
        cell_height = 42

        rows = max(1, (grid_bottom - grid_top + gap) // (cell_height + gap))
        page_size = columns * rows
        page_start = self.grid_offset * page_size
        page_end = min(page_start + page_size, len(self.items))

        font = self.display.get_font(FONT_SIZE_MENU_ITEM)

        for position, index in enumerate(range(page_start, page_end)):
            row, column = divmod(position, columns)
            x = grid_left + column * (cell_width + gap)
            y = grid_top + row * (cell_height + gap)
            item = self.items[index]
            label = textwrap.shorten(item.text, width=18, placeholder="...")
            selected = index == self.selected

            if selected:
                draw.rectangle(
                    (x, y, x + cell_width, y + cell_height),
                    outline=0,
                    width=2,
                )

            bbox = draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = x + max(4, (cell_width - text_width) // 2)
            text_y = y + (cell_height - (bbox[3] - bbox[1])) // 2 - bbox[1]
            item_color = self.display.epd.GRAY3 if item.text == "Back" else 0

            draw.text((text_x, text_y), label, font=font, fill=item_color)

        if len(self.items) > page_size:
            track_top = grid_top
            track_bottom = grid_bottom
            track_height = track_bottom - track_top
            pages = (len(self.items) + page_size - 1) // page_size
            scrollbar_height = max(10, track_height // pages)
            scrollbar_y = track_top + int(
                (track_height - scrollbar_height)
                * self.grid_offset
                / max(1, pages - 1)
            )
            draw.rectangle(
                (self.display.height - 8, scrollbar_y,
                 self.display.height - 4, scrollbar_y + scrollbar_height),
                fill=0,
            )

    def handle_grid_input(self, event):
        columns = 3
        rows = max(
            1,
            (self.display.width - self.menu_start_y - 35 + 10) // (42 + 10),
        )
        old_selected = self.selected

        if event == Event.RIGHT:
            self.selected = min(self.selected + 1, len(self.items) - 1)
        elif event == Event.LEFT:
            if self.selected % columns == 0:
                self.back()
                return
            self.selected -= 1
        elif event == Event.DOWN:
            self.selected = min(self.selected + columns, len(self.items) - 1)
        elif event == Event.UP:
            self.selected = max(self.selected - columns, 0)
        elif event == Event.SELECT:
            item = self.items[self.selected]
            if item.screen is not None:
                self.ui.show(item.screen)
            elif item.action is not None:
                item.action()
            return
        else:
            return

        if self.selected != old_selected:
            page_size = columns * rows
            self.grid_offset = self.selected // page_size
            self.show()
