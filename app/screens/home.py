from app.core.events import Event
from app.reader import book_reader
from app.screen import Screen
from app.screens.main_menu import MainMenu


class HomeScreen(Screen):

    def __init__(self, display, assets_dir=None, ui=None, book_reader=None, app=None):
        super().__init__(display, assets_dir, ui, book_reader, app)

    def show(self):
        image_path = self.assets_dir / "images" / "raspreader_home.bmp"
        self.display.show_image(str(image_path))

        self.display.use_fast_mode()

    def handle_input(self, event):
        if event == Event.SELECT:
            self.ui.show(MainMenu)