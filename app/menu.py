from dataclasses import dataclass

from PIL import ImageFont

from app.events import Event
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

        y = 70

        for i, item in enumerate(self.items):

            prefix = "▶ " if i == self.selected else "  "

            draw.text(
                (20, y),
                prefix + item.text,
                font=self.display.get_font(18),
                fill=0,
            )

            y += 35

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