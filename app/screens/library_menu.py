from app.widgets.menu import MenuItem, MenuScreen


class LibraryScreen(MenuScreen):

    def __init__(
        self,
        display,
        assets_dir=None,
        ui=None,
        library=None,
    ):

        self.library = library

        books = self.library.get_books()

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
        )


    def select_book(self, book):

        print("=== Book selected ===")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")


    def back(self):

        from app.screens.main_menu import MainMenu

        self.ui.show(MainMenu)