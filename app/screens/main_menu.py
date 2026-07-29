from app.menu import MenuItem, MenuScreen
from app.screens.settings_menu import SettingsScreen
from app.screens.library_menu import LibraryScreen


class MainMenu(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Main Menu",
            items=[
                MenuItem("Library", screen=LibraryScreen),
                MenuItem("Settings", screen=SettingsScreen),
                MenuItem("About", action=self.about),
            ],
        )

    def about(self):
        print("About selected")

    def back(self):
        from app.screens.home import HomeScreen
        self.ui.show(HomeScreen)