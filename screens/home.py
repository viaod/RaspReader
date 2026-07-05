from .screen import Screen


class HomeScreen(Screen):

    def show(self):

        self.display.show_image(
            self.assets / "images" / "raspreader_home.bmp"
        )