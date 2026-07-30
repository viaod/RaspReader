from app.widgets.menu import MenuItem, MenuScreen

from app.widgets.menu import MenuItem, MenuScreen

class LibraryScreen(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Library",
            items=[
                MenuItem("Dracula", action=self.select_book),
                MenuItem("The Odyssey", action=self.select_book),
                MenuItem("Pride and Prejudice", action=self.select_book),
                MenuItem("Hunger Games", action=self.select_book),
                MenuItem("Back", action=self.back),
            ],
        )

    def select_book(self):
        print("=== Book selected ===")

    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)