from app.widgets.menu import MenuItem, MenuScreen
from app.screens.settings_menu import SettingsScreen
from app.screens.library_menu import LibraryScreen


class MainMenu(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None, **kwargs):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Main Menu",
            items=[
                MenuItem("Library", screen=LibraryScreen),
                MenuItem("Continue Reading", action=self.continue_reading),
                MenuItem("Bookmarks", action=self.bookmarks),
                MenuItem("Dictionary", action=self.dictionary),
                MenuItem("Settings", screen=SettingsScreen),
            ],
            **kwargs
        )

    def continue_reading(self):
        print("Continue Reading")
    
    def bookmarks(self):
        print("Bookmarks")
        
    def dictionary(self):
        print("Dictionary")

    def back(self):
        from app.screens.home import HomeScreen
        self.ui.show(HomeScreen)