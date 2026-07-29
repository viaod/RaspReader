from app.menu import MenuItem, MenuScreen

from app.menu import MenuItem, MenuScreen

class LibraryScreen(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Library",
            items=[
                MenuItem("Display", action=self.display_settings),
                MenuItem("WiFi", action=self.wifi_settings),
                MenuItem("Back", action=self.back),
            ],
        )

    def display_settings(self):
        print("Display")

    def wifi_settings(self):
        print("WiFi")

    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)