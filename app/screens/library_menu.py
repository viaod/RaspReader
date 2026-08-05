from app.widgets.menu import MenuItem, MenuScreen
from app.core.logger import Logger


logger = Logger("LibraryScreen")


class LibraryScreen(MenuScreen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        app=None
    ):

        self.app = app

        books = self.app.library.get_books()
         
        # books = sorted(
        #     self.app.library.get_books(),
        #     key=lambda book: book.title.lower()
        # )

        items = []

        for book in books:
            items.append(
                MenuItem(
                    book.title,
                    action=lambda b=book: self.select_book(b)
                )
            )

        items.append(
            MenuItem(
                "Back",
                action=self.back
            )
        )

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Library",
            items=items,
            app=app,
        )


    def select_book(self, book):

        logger.info("Selected book: %s", book.title)
        self.app.selected_book = book

        from app.screens.reader_menu import ReaderMenu

        self.ui.show(ReaderMenu)


    def back(self):

        from app.screens.main_menu import MainMenu

        self.ui.show(MainMenu)