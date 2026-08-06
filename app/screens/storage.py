import shutil

from app.core.events import Event
from app.screen import Screen


class StorageScreen(Screen):

    def draw_centered(self, text, y, font):
        bbox = self.display.draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.display.height - text_width) // 2
        self.display.draw.text((x, y), text, font=font, fill=0)

    def show(self):
        total, used, free = shutil.disk_usage("/")

        percent = used / total

        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)

        self.display.clear_image()
        self.draw_status_header()

        font_title = self.display.get_font(22)
        font = self.display.get_font(18)

        # Title
        self.display.draw.text(
            (20, 20),
            "Storage",
            font=font_title,
            fill=0,
        )

        # Progress bar
        width = 180
        height = 20
        x = (self.display.height - width) // 2
        y = 70

        self.display.draw.rectangle(
            (x, y, x + width, y + height),
            outline=0,
            width=2,
        )

        filled = int(width * percent)

        if filled > 0:
            self.display.draw.rectangle(
                (x + 2, y + 2, x + filled - 2, y + height - 2),
                fill=(255, 0, 0),
            )

        # Storage information
        self.draw_centered(
            f"Used: {used_gb:.1f} / {total_gb:.1f} GB",
            105,
            font,
        )

        self.draw_centered(
            f"Free: {free_gb:.1f} GB",
            135,
            font,
        )

        self.draw_centered(
            f"{percent * 100:.0f}% used",
            165,
            font,
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
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)