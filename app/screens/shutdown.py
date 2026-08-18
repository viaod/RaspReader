import subprocess
import time

from app.core.events import Event
from app.screen import Screen
from app.core.config import FONT_SIZE_SCREEN_BODY, FONT_SIZE_SCREEN_TITLE


class ShutdownScreen(Screen):

    def show(self):

        self.display.clear_image()
        self.draw_status_header()

        title_font = self.display.get_font(FONT_SIZE_SCREEN_TITLE)
        font = self.display.get_font(FONT_SIZE_SCREEN_BODY)

        self.display.draw.text(
            (20, 25),
            "Shutdown?",
            font=title_font,
            fill=0,
        )

        self.display.draw.text(
            (20, 70),
            "Press SELECT",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 95),
            "to power off.",
            font=font,
            fill=0,
        )

        self.display.draw.text(
            (20, 170),
            "LEFT = Cancel",
            font=font,
            fill=0,
        )

        self.display.refresh()

    def handle_input(self, event):

        if event == Event.LEFT:
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)

        elif event == Event.SELECT:
            self.power_off()

    def power_off(self):
        # Ensure the display is fully cleared (hardware full-clear when
        # supported) and put to sleep before powering off so no image
        # remains visible after shutdown.
        try:
            if self.display:
                try:
                    # Prefer full clear if available
                    self.display.clear(force_full=True)
                except TypeError:
                    # older signature
                    try:
                        self.display.clear()
                    except Exception:
                        pass
                except Exception:
                    # best-effort: try simple clear
                    try:
                        self.display.clear()
                    except Exception:
                        pass

                try:
                    self.display.sleep()
                except Exception:
                    pass

        except Exception:
            # Do not block shutdown on display errors
            pass

        time.sleep(1)

        subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)