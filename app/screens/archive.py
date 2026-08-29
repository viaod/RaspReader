from app.core.logger import Logger
from app.widgets.menu import MenuItem, MenuScreen


logger = Logger("Archive")


class ArchiveScreen(MenuScreen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        app=None,
    ):

        self.app = app

        books = self.app.library.get_offloaded_books()

        items = []

        if books:

            for book in books:

                items.append(
                    MenuItem(
                        book.title,
                        action=lambda b=book: self.restore_book(b)
                    )
                )

        else:

            items.append(
                MenuItem(
                    "Archive is empty",
                    action=lambda: None
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
            title="Archive",
            items=items,
            app=app,
        )


    def restore_book(self, book):

        logger.info(f"Restoring book: {book.title}")

        self.app.library.restore_book(book)

        from app.screens.library_menu import LibraryScreen

        self.ui.show(LibraryScreen)


    def back(self):

        from app.screens.main_menu import MainMenu

        self.ui.show(MainMenu)