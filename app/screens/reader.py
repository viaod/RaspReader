from app.screen import Screen
from app.core.events import Event


class ReaderScreen(Screen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        app=None,
    ):

        super().__init__(
            display,
            assets_dir,
            ui,
            app=app,
        )

        self.app = app
        self.book_reader = app.book_reader


    def show(self):

        self.display.clear_image()

        page = self.book_reader.current_page()

        if page is None:
            return


        draw = self.display.draw

        font = self.display.get_font(20)

        y = 20

        for line in page.text.split("\n"):

            draw.text(
                (10, y),
                line,
                font=font,
                fill=0,
            )

            y += 20


        # footer
        draw.text(
            (10, 220),
            f"Page {page.number}",
            font=self.display.get_font(14),
            fill=0,
        )


        self.display.refresh()


    def handle_input(self, event):

        if event == Event.DOWN:
            self.book_reader.next_page()
            self.show()


        elif event == Event.UP:
            self.book_reader.previous_page()
            self.show()


        elif event == Event.LEFT:
            from app.screens.library_menu import LibraryScreen
            self.ui.show(LibraryScreen)