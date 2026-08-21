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
                MenuItem("Library", screen=LibraryScreen),
                MenuItem("Continue Reading", action=self.continue_reading),
                MenuItem("Bookmarks", action=self.bookmarks),
                # MenuItem("Dictionary X", action=self.dictionary),
                # MenuItem("Archive X", action=self.archive),
                MenuItem("Settings", screen=SettingsScreen),
            ],
            app=app,
            )

    def continue_reading(self):
        logger.info("Continue Reading selected")
    
    def bookmarks(self):
        logger.info("Bookmarks selected")
        from app.screens.bookmarks import BookmarkBooksScreen
        self.ui.show(BookmarkBooksScreen)
        
    # def dictionary(self):
    #     logger.info("Dictionary selected")
        
    # def archive(self):
    #     logger.info("Archive selected")

    def back(self):
        from app.screens.home import HomeScreen
        self.ui.show(HomeScreen)
