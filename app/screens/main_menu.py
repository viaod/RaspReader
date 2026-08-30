from app.widgets.menu import MenuItem, MenuScreen
from app.screens.settings_menu import SettingsScreen
from app.screens.library_menu import LibraryScreen
from app.core.logger import Logger


logger = Logger("MainMenu")


class MainMenu(MenuScreen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        title="Menu",
        items=None,
        app=None,
    ):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Main Menu",
            items=[
                MenuItem("Continue Reading", action=self.continue_reading),
                MenuItem("Library", screen=LibraryScreen),
                MenuItem("Bookmarks", action=self.bookmarks),
                # MenuItem("Dictionary X", action=self.dictionary),
                MenuItem("Archive", action=self.archive),
                MenuItem("Settings", screen=SettingsScreen),
            ],
            app=app,
            )

    def continue_reading(self):
        logger.info("Continue Reading selected")

        progress = self.app.book_reader.progress

        candidate_keys = []
        last_book = progress.get_last_book()
        if last_book:
            candidate_keys.append(last_book)

        latest_book = progress.get_latest_book()
        if latest_book and latest_book not in candidate_keys:
            candidate_keys.append(latest_book)

        for key in candidate_keys:
            book = self._find_book_by_key(key)
            if book:
                if self.app.library.state.is_offloaded(book):
                    self.app.library.restore_book(book)

                self.app.selected_book = book
                self.app.book_reader.open(book)

                from app.screens.reader import ReaderScreen
                self.ui.show(ReaderScreen)
                return

        logger.info("No previous book found")
    
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