from pathlib import Path

from app.screen import Screen


class HomeScreen(Screen):
    def __init__(self, display, assets_dir=None):
        super().__init__(display, assets_dir)

    def show(self):
        image_path = self.assets_dir / "images" / "raspreader_home.bmp"
        self.display.show_image(str(image_path))
