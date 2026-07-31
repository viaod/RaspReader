import shutil

from app.core.events import Event
from app.screen import Screen


class StorageScreen(Screen):

    def show(self):
        total, used, free = shutil.disk_usage("/")

        percent = used / total

        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)

        self.display.clear_image()

        font_title = self.display.get_font(22)
        font = self.display.get_font(18)

        self.display.draw.text(
            (20, 20),
            "Storage",
            font=font_title,
            fill=0,
        )

        # Progress bar
        x = 20
        y = 70
        width = 180
        height = 20

        self.display.draw.rectangle(
            (x, y, x + width, y + height),
            outline=0,
            width=2,
        )

        filled = int(width * percent)

        if filled > 0:
            self.display.draw.rectangle(
                (x + 2, y + 2, x + filled - 2, y + height - 2),
                fill=0,
            )

        self.display.draw.text(
            (20, 105),
            f"Used: {used_gb:.1f} / {total_gb:.1f} GB",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 135),
            f"Free: {free_gb:.1f} GB",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 165),
            f"{percent*100:.0f}% used",
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
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)