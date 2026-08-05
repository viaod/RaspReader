from app.core.logger import Logger
from app.widgets.menu import MenuItem, MenuScreen


logger = Logger("ReaderMenu")


class ReaderMenu(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None, app=None):

        self.book = app.selected_book

        if self.book is None:
            raise RuntimeError("ReaderMenu requires a selected book.")

        self.book_reader = app.book_reader
        self.cache_exists = self.book_reader.book_cache.exists(self.book)

        primary_action = "Continue Reading" if self.cache_exists else "Start Reading"
        items = [MenuItem(primary_action, action=self.open_book)]

        if self.cache_exists:
            items.append(MenuItem("Delete Cache", action=self.delete_cache))

        items.append(MenuItem("Delete Book", action=self.delete_book))
        items.append(MenuItem("Back", action=self.back))

        super().__init__(
            display,
            assets_dir,
            ui,
            title=self.book.title,
            items=items,
            app=app,
        )

    def open_book(self):

        logger.info("Opening '%s' from reader menu", self.book.title)
        self.book_reader.open(self.book)

        from app.screens.reader import ReaderScreen

        self.ui.show(ReaderScreen)

    def delete_cache(self):

        if self.book_reader.book_cache.delete(self.book):
            self.book_reader.progress.clear_position(self.book.title)
            logger.info("Deleted cache and reading position for '%s'", self.book.title)
        else:
            logger.warning("No cache found to delete for '%s'", self.book.title)

        self.ui.show(ReaderMenu)

    def delete_book(self):

        if self.app.library.remove_book(self.book.path.name):
            self.book_reader.book_cache.delete(self.book)
            self.book_reader.progress.clear_position(self.book.title)
            self.app.selected_book = None
            logger.info("Deleted book, cache, and reading position: '%s'", self.book.title)
        else:
            logger.warning("Book was not found for deletion: '%s'", self.book.title)

        from app.screens.library_menu import LibraryScreen

        self.ui.show(LibraryScreen)

    def back(self):

        from app.screens.library_menu import LibraryScreen

        self.ui.show(LibraryScreen)
