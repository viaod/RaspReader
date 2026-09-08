from functools import cache

from app.widgets.menu import MenuItem, MenuScreen
from app.core.logger import Logger
import textwrap

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
        progress = self.app.book_reader.progress.load()
        book_cache = self.app.book_reader.book_cache

        items = []
        
        # cached_book = self.book_cache.load(book)

        # if cached_book:
        #     self.book = cached_book
        #     logger.info("Loaded book from cache: %s", self.book.title)

        for book in books:
            label = textwrap.shorten(book.title, width=35, placeholder="...")
            position = progress.get(str(book.title))
            if position is not None:
                cached_book = book_cache.load(book)
                total_pages = sum(
                    len(chapter.pages)
                    for chapter in cached_book.chapters
                ) if cached_book else 0

                if total_pages:
                    percentage = min(
                        100,
                        round(100 * (position.get("page", 0) + 1) / total_pages),
                    )
                    label = f"{label} [{percentage}%]"
                else:
                    label = f"{label} [In progress]"

            items.append(
                MenuItem(
                    label,
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
            grid=False,
        )

    def select_book(self, book):

        logger.info("Selected book: %s", book.title)
        self.app.selected_book = book

        from app.screens.reader_menu import ReaderMenu

        self.ui.show(ReaderMenu)


    def back(self):

        from app.screens.main_menu import MainMenu

        self.ui.show(MainMenu)