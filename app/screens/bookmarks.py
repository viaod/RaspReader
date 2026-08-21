import textwrap

from app.core.events import Event
from app.core.logger import Logger
from app.widgets.menu import MenuItem, MenuScreen


logger = Logger("Bookmarks")


class BookmarkBooksScreen(MenuScreen):
    """List library books that have one or more saved bookmarks."""

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        self.app = app
        bookmarks_by_book = app.book_reader.bookmarks.load()
        books = [
            book for book in app.library.get_books()
            if bookmarks_by_book.get(book.title)
        ]

        items = [
            MenuItem(
                textwrap.shorten(book.title, width=45, placeholder="..."),
                action=lambda b=book: self.select_book(b),
            )
            for book in books
        ]

        if not items:
            items.append(MenuItem("No bookmarks saved"))

        items.append(MenuItem("Back", action=self.back))

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Bookmarks",
            items=items,
            app=app,
        )

    def select_book(self, book):
        self.app.selected_book = book
        logger.info("Selected bookmarked book: %s", book.title)

        self.ui.show(BookmarkPagesScreen)

    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)


class BookmarkPagesScreen(MenuScreen):
    """List the saved bookmark positions for the selected book."""

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        self.app = app
        self.book = app.selected_book
        self.bookmarks = app.book_reader.bookmarks.get_bookmarks(self.book.title)
        self.bookmarks.sort(key=lambda bookmark: bookmark["page"])

        items = [
            MenuItem(
                f"Page {bookmark['page'] + 1} (Chapter {bookmark['chapter'] + 1})",
                action=lambda b=bookmark: self.open_bookmark(b),
            )
            for bookmark in self.bookmarks
        ]
        items.append(MenuItem("Back", action=self.back))

        super().__init__(
            display,
            assets_dir,
            ui,
            title=textwrap.shorten(self.book.title, width=32, placeholder="..."),
            items=items,
            app=app,
        )

    def handle_input(self, event):
        if event == Event.RIGHT and self.selected < len(self.bookmarks):
            bookmark = self.bookmarks[self.selected]
            self.app.book_reader.bookmarks.remove(
                self.book.title,
                bookmark["chapter"],
                bookmark["page"],
            )
            logger.info(
                "Removed bookmark from '%s', page %d",
                self.book.title,
                bookmark["page"] + 1,
            )

            if len(self.bookmarks) == 1:
                self.ui.show(BookmarkBooksScreen)
            else:
                self.ui.show(BookmarkPagesScreen)
            return

        super().handle_input(event)

    def open_bookmark(self, bookmark):
        self.app.book_reader.open(self.book)

        if not self.app.book_reader.go_to_page(bookmark["page"]):
            logger.warning(
                "Bookmark page %d is no longer available in '%s'",
                bookmark["page"] + 1,
                self.book.title,
            )
            return

        logger.info(
            "Opening bookmark in '%s', page %d",
            self.book.title,
            bookmark["page"] + 1,
        )
        from app.screens.reader import ReaderScreen
        self.ui.show(ReaderScreen)

    def back(self):
        self.ui.show(BookmarkBooksScreen)
