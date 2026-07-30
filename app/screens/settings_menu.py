import subprocess

from app.widgets.menu import MenuItem, MenuScreen
from app.screens.storage import StorageScreen
from app.screens.shutdown import ShutdownScreen


class SettingsScreen(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Settings",
            items=[
                MenuItem("Upload", action=self.upload_setting),
                MenuItem("Storage", screen=StorageScreen),
                MenuItem(
                    f"WiFi: {'On' if self.wifi_enabled() else 'Off'}",
                    action=self.wifi_settings,
                ),
                MenuItem("Back", action=self.back),
                MenuItem("Shutdown", action=self.shutdown),
            ],
        )

    def upload_setting(self):
        print("Uploading...")
        
    def storage_settings(self):
        self.ui.show(StorageScreen)

    def wifi_settings(self):
        try:
            if self.wifi_enabled():
                subprocess.run(
                    ["sudo", "rfkill", "block", "wifi"],
                    check=True,
                )
                print("WiFi disabled")
            else:
                subprocess.run(
                    ["sudo", "rfkill", "unblock", "wifi"],
                    check=True,
                )
                print("WiFi enabled")

            # Update the menu text
            self.items[2].text = (
                f"WiFi: {'On' if self.wifi_enabled() else 'Off'}"
            )
            self.show()

        except subprocess.CalledProcessError as e:
            print(f"Failed to toggle WiFi: {e}")

    def wifi_enabled(self):
        result = subprocess.run(
            ["rfkill", "list", "all"],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = result.stdout.splitlines()

        for i, line in enumerate(lines):
            if "Wireless LAN" in line:
                return "Soft blocked: no" in lines[i + 1]

        return False
    
    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)
        
    def shutdown(self):
        self.ui.show(ShutdownScreen)