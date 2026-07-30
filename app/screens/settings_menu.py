from app.widgets.menu import MenuItem, MenuScreen

class SettingsScreen(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Settings",
            items=[
                MenuItem("Upload", action=self.upload_setting),
                MenuItem("Storage", action=self.storage_settings),
                MenuItem("Toggle WiFi", action=self.wifi_settings),
                MenuItem("Back", action=self.back),
            ],
        )

    def upload_setting(self):
        print("Uploading...")
        
    def storage_settings(self):
        print("Storage")

    def wifi_settings(self):
        print("WiFi")

    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)