from app.core.events import Event
from app.reader import book_reader
from app.screen import Screen
from app.screens.main_menu import MainMenu
from PIL import Image, ImageDraw


class HomeScreen(Screen):

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        super().__init__(display, assets_dir, ui, app)

    def show(self):
        image_path = self.assets_dir / "images" / "raspreader_home.bmp"

        img = Image.open(str(image_path)).convert("L")
        img = img.resize((self.display.height, self.display.width))

        # Replace the display's current canvas with the composed image
        self.display.image = img
        self.display.draw = ImageDraw.Draw(self.display.image)

        # Keep the shared status text readable over the home artwork.
        self.display.draw.rectangle(
            (0, 0, self.display.height, 24),
            fill=255,
        )

        # Draw the shared header on top of the white band.
        self.draw_status_header()

        # Single update to the hardware
        self.display.show(self.display.image)

    def handle_input(self, event):
        if event == Event.SELECT:
            self.ui.show(MainMenu)
