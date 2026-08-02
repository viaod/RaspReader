from app.widgets.menu import MenuItem, MenuScreen


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
        
        self.app.book_reader.open(book)

        from app.screens.reader import ReaderScreen

        self.ui.show(
            ReaderScreen
        )


    def back(self):

        from app.screens.main_menu import MainMenu

        self.ui.show(MainMenu)