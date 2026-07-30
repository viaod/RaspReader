from app.core.events import Event
from app.screen import Screen
from app.screens.main_menu import MainMenu


class HomeScreen(Screen):

    def __init__(self, display, assets_dir=None, ui=None):
        super().__init__(display, assets_dir, ui)

    def show(self):
        print(f"assets_dir = {self.assets_dir}")

        image_path = self.assets_dir / "images" / "raspreader_home.bmp"
        print(f"image_path = {image_path}")
        print(f"exists = {image_path.exists()}")

        self.display.show_image(str(image_path))
        self.display.use_fast_mode()

    def handle_input(self, event):
        if event == Event.SELECT:
            self.ui.show(MainMenu)