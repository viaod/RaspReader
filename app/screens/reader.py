from app.screen import Screen
from app.core.events import Event
from app.core.logger import Logger


logger = Logger("ReaderScreen")


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
        self.draw_status_header()

        page = self.book_reader.current_page()

        if page is None:
            logger.warning("Reader screen opened without a current page")
            return

        logger.debug("Rendering page %d", page.number)


        draw = self.display.draw

        font = self.display.get_font(26)

        y = 30

        for line in page.text.split("\n"):

            draw.text(
                (10, y),
                line,
                font=font,
                fill=0,
            )

            y += 20


        # Footer: page number on the left and reading progress on the right.
        footer_font = self.display.get_font(14)
        draw.text(
            (10, 220),
            f"Page {page.number}",
            font=footer_font,
            fill=0,
        )

        total_pages = len(self.book_reader.pages)
        progress_percent = round(((self.book_reader.page_index + 1) / total_pages) * 100)
        progress_text = f"{progress_percent}%"
        progress_width = draw.textlength(progress_text, font=footer_font)
        draw.text(
            (self.display.height - progress_width - 10, 220),
            progress_text,
            font=footer_font,
            fill=0,
        )


        self.display.refresh()


    def handle_input(self, event):

        if event == Event.RIGHT:
            self.book_reader.next_page()
            self.show()


        elif event == Event.LEFT:
            self.book_reader.previous_page()
            self.show()


        elif event == Event.SELECT:
            from app.screens.reader_menu import ReaderMenu
            self.ui.show(ReaderMenu)
