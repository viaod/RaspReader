import shutil
from pathlib import Path

from app.core.events import Event
from app.screen import Screen
from app.core.config import FONT_SIZE_SCREEN_BODY, FONT_SIZE_SCREEN_TITLE


class StorageScreen(Screen):

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        super().__init__(display, assets_dir, ui, app)
        self.selected = 0

    def draw_centered(self, text, y, font):
        bbox = self.display.draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.display.height - text_width) // 2
        self.display.draw.text((x, y), text, font=font, fill=0)

    def draw_bottom_menu(self, font):
        footer_y = 216
        self.display.draw.line((10, footer_y - 8, self.display.height - 10, footer_y - 8), fill=0)

        left_text = "Clear Data"
        right_text = "Back"

        if self.selected == 0:
            left_text = "▶ Clear Data"
        else:
            right_text = "▶ Back"

        left_x = 18
        right_x = self.display.height - self.display.draw.textlength(right_text, font=font) - 18

        self.display.draw.text((left_x, footer_y), left_text, font=font, fill=0)
        self.display.draw.text((right_x, footer_y), right_text, font=font, fill=0)

    def clear_data(self):
        from app.screens.clear_data_menu import ClearDataMenu
        self.ui.show(ClearDataMenu)

    def back(self):
        from app.screens.settings_menu import SettingsScreen
        self.ui.show(SettingsScreen)

    def show(self):
        total, used, free = shutil.disk_usage("/")

        percent = used / total

        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)

        self.display.clear_image()
        self.draw_status_header()

        font_title = self.display.get_font(FONT_SIZE_SCREEN_TITLE)
        font = self.display.get_font(FONT_SIZE_SCREEN_BODY)

        self.draw_centered("Storage", 25, font_title)

        width = 180
        height = 20
        x = (self.display.height - width) // 2
        y = 70

        self.display.draw.rectangle((x, y, x + width, y + height), outline=0, width=2)

        filled = int(width * percent)
        if filled > 0:
            self.display.draw.rectangle((x + 2, y + 2, x + filled - 2, y + height - 2), fill=0)

        self.draw_centered(f"Used: {used_gb:.1f} / {total_gb:.1f} GB", 105, font)
        self.draw_centered(f"Free: {free_gb:.1f} GB", 135, font)
        self.draw_centered(f"{percent * 100:.0f}% used", 165, font)

        self.draw_bottom_menu(font)
        self.display.refresh()

    def handle_input(self, event):
        if event == Event.LEFT:
            self.selected = 0 if self.selected == 0 else self.selected - 1
            self.show()
        elif event == Event.RIGHT:
            self.selected = 1 if self.selected == 0 else 1
            self.show()
        elif event == Event.SELECT:
            if self.selected == 0:
                self.clear_data()
            else:
                self.back()
        elif event == Event.UP:
            self.back()