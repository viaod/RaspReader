import os
import subprocess
from pathlib import Path

from app.screens.upload import UploadScreen
from app.widgets.menu import MenuItem, MenuScreen
from app.screens.storage import StorageScreen
from app.screens.shutdown import ShutdownScreen
from app.screens.font_settings import FontSettingsScreen
from app.core.logger import Logger


logger = Logger("Settings")


class SettingsScreen(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None, app=None):

        super().__init__(
            display,
            assets_dir,
            ui,
            title="Settings",
            items=[
                MenuItem("Upload", screen=UploadScreen),
                MenuItem("Storage", screen=StorageScreen),
                MenuItem("Device Font", screen=FontSettingsScreen),
                MenuItem("Check for Updates", action=self.check_for_updates),
                MenuItem(
                    f"WiFi: {'On' if self.wifi_enabled() else 'Off'}",
                    action=self.wifi_settings,
                ),
                MenuItem("Back", action=self.back),
                MenuItem("Shutdown", screen=ShutdownScreen),
            ],
            app=app
        )

    def check_for_updates(self):
        repo_dir = Path(__file__).resolve().parents[2]
        venv_python = Path.home() / "myenv" / "bin" / "python"

        try:
            subprocess.run(
                ["git", "pull", "--ff-only"],
                cwd=str(repo_dir),
                check=True,
                capture_output=True,
                text=True,
            )

            if self.display is not None:
                self.display.clear_image()
                self.display.refresh()

            subprocess.Popen(
                [str(venv_python), "-m", "main"],
                cwd=str(repo_dir),
            )
            os._exit(0)

        except subprocess.CalledProcessError as exc:
            logger.error("Update failed: %s", exc)

    def wifi_settings(self):
        try:
            if self.wifi_enabled():
                subprocess.run(
                    ["sudo", "rfkill", "block", "wifi"],
                    check=True,
                )
                logger.info("WiFi disabled")
            else:
                subprocess.run(
                    ["sudo", "rfkill", "unblock", "wifi"],
                    check=True,
                )
                logger.info("WiFi enabled")

            # Update the WiFi menu item without depending on its position.
            for item in self.items:
                if item.text.startswith("WiFi:"):
                    item.text = f"WiFi: {'On' if self.wifi_enabled() else 'Off'}"
                    break
            self.show()

        except subprocess.CalledProcessError as e:
            logger.error("Failed to toggle WiFi: %s", e)

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
    
