from app.widgets.menu import MenuItem, MenuScreen
from app.screens.settings_menu import SettingsScreen
from app.screens.library_menu import LibraryScreen
from app.core.logger import Logger


logger = Logger("MainMenu")


class MainMenu(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None, title="Menu", items=None, app=None):
        super().__init__(
            display,
            assets_dir,
            ui,
            title="Main Menu",
            items=[],
            app=app,
        )

        self._prev_book = self._get_prev_book_if_any()

        menu_items = [
            MenuItem("Library", screen=LibraryScreen),
            MenuItem("Bookmarks", action=self.bookmarks),
            MenuItem("Archive", action=self.archive),
            MenuItem("Settings", screen=SettingsScreen),
        ]

        if self._prev_book is not None:
            menu_items.insert(
                0,
                MenuItem(f"Continue Reading: {self._prev_book.title}", action=self.continue_reading),
            )

        self.items = menu_items

    def _get_prev_book_if_any(self):
        if self.app is None or self.app.book_reader is None:
            return None

        progress = self.app.book_reader.progress
        last_book_key = progress.get_last_book()
        if not last_book_key:
            return None

        book = self._find_book_by_key(last_book_key)
        if book is None:
            return None

        if self.app.library.state.is_offloaded(book):
            self.app.library.restore_book(book)

        return book

    def continue_reading(self):
        book = self._get_prev_book_if_any()
        if not book:
            logger.info("No previous book found")
            return

        self.app.selected_book = book
        self.app.book_reader.open(book)

        from app.screens.reader import ReaderScreen
        self.ui.show(ReaderScreen)
    
    def bookmarks(self):
        logger.info("Bookmarks selected")
        from app.screens.bookmarks import BookmarkBooksScreen
        self.ui.show(BookmarkBooksScreen)
        
    # def dictionary(self):
    #     logger.info("Dictionary selected")
        
    def archive(self):
        logger.info("Archive selected")
        
        from app.screens.archive import ArchiveScreen
        self.ui.show(ArchiveScreen)

    def back(self):
        from app.screens.home import HomeScreen
        self.ui.show(HomeScreen)

    def _find_book_by_key(self, key):
        key = str(key)

        for book in self.app.library.get_books():
            if str(book.path.name) == key or str(book.path) == key or book.title == key:
                return book

        for book in self.app.library.get_offloaded_books():
            if str(book.path.name) == key or str(book.path) == key or book.title == key:
                return book

        return None