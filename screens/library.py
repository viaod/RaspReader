import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from books.library import Library
from books.parser import Parser
from screens.screen import Screen


class LibraryScreen(Screen):
    def __init__(self, display):
        super().__init__(display)

        self.library = Library()
        self.current_book_index = 0
        self.current_page_index = 0
        self.selected = 0
        self.start_index = 0
        self.visible_items = 7
        self.font = ImageFont.load_default()
        self.title_font = ImageFont.load_default()
        self.book_count = len(getattr(self.library, "file_names", []))
        self.book_titles = self.get_book_titles()

    def get_book_titles(self):
        titles = []

        for book_name in getattr(self.library, "file_names", []):
            try:
                parser = Parser(book_name)
                title = parser.metadata.get("title") or Path(book_name).stem
            except Exception:
                title = Path(book_name).stem

            titles.append(title)

        return titles

    def draw(self):
        image = Image.new(
            "1",
            (self.display.epd.height, self.display.epd.width),
            255,
        )

        draw = ImageDraw.Draw(image)

        draw.text((15, 15), "Library", font=self.title_font, fill=0)
        draw.line((15, 38, 400, 38), fill=0)

        display_width = self.display.epd.height
        y = 60

        if self.start_index > 0:
            draw.text((350, 45), "^", font=self.font, fill=0)

        visible_books = self.book_titles[self.start_index:self.start_index + self.visible_items]

        for i, title in enumerate(visible_books):
            padding = 10
            text_width = draw.textlength(title, font=self.font)
            x = (display_width - text_width) / 2
            row_y = y + i * 35

            if self.start_index + i == self.selected:
                draw.rectangle(
                    (
                        x - padding,
                        row_y - 2,
                        x + text_width + padding,
                        row_y + 18,
                    ),
                    outline=0,
                    width=2,
                )

            draw.text((x, row_y), title, font=self.font, fill=0)

        wifi = self.get_wifi_status()
        ip = self.get_ip()

        draw.line((0, 215, 415, 215), fill=0)
        draw.text((10, 222), wifi, font=self.font, fill=0)

        w = draw.textlength(ip, font=self.font)
        draw.text((415 - w - 10, 222), ip, font=self.font, fill=0)

        if self.start_index + self.visible_items < len(self.book_titles):
            draw.text((350, 222), "v", font=self.font, fill=0)

        self.display.show(image)

    def handle_input(self, event):
        if event == "clockwise":
            if self.book_titles:
                if self.selected < len(self.book_titles) - 1:
                    self.selected += 1
                    if self.selected >= self.start_index + self.visible_items:
                        self.start_index += 1
                else:
                    self.selected = 0
                    self.start_index = 0
            return True

        if event == "counter_clockwise":
            if self.book_titles:
                if self.selected > 0:
                    self.selected -= 1
                    if self.selected < self.start_index:
                        self.start_index -= 1
                else:
                    self.selected = len(self.book_titles) - 1
                    self.start_index = max(0, len(self.book_titles) - self.visible_items)
            return True

        if event == "select":
            if self.book_titles:
                return self.book_titles[self.selected]
            return None

        return None

    def get_wifi_status(self):
        try:
            result = subprocess.check_output(
                ["cat", "/sys/class/net/wlan0/operstate"],
                text=True,
            ).strip()

            if result == "up":
                return "WiFi [ON]"

            return "WiFi [OFF]"

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

    def show(self):
        self.draw()       
