from pathlib import Path

from PIL import ImageFont

from app.core.events import Event
from app.core.config import FONT_SIZE_SCREEN_BODY, FONT_SIZE_SCREEN_TITLE
from app.screen import Screen


class FontSettingsScreen(Screen):
    """Preview and select a device-wide font from assets/fonts."""

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        super().__init__(display, assets_dir, ui, app)
        project_dir = Path(__file__).resolve().parents[2]
        fonts_dir = Path(assets_dir or project_dir / "assets") / "fonts"
        self.font_paths = sorted(
            path
            for extension in ("*.ttf", "*.otf", "*.ttc")
            for path in fonts_dir.glob(extension)
        )
        current_path = Path(getattr(display, "font_path", "")).resolve()
        self.selected = next(
            (index for index, path in enumerate(self.font_paths) if path.resolve() == current_path),
            0,
        )

    def show(self):
        self.display.clear_image()
        self.draw_status_header()
        draw = self.display.draw
        title_font = self.display.get_font(FONT_SIZE_SCREEN_TITLE)
        body_font = self.display.get_font(FONT_SIZE_SCREEN_BODY)

        title = "Device Font"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = (self.display.height - title_width) // 2
        draw.text((title_x, 25), title, font=title_font, fill=0)
        draw.line((15, 48, self.display.height - 15, 48), fill=0)

        if not self.font_paths:
            draw.text((20, 75), "No fonts found in assets/fonts", font=body_font, fill=0)
        else:
            font_path = self.font_paths[self.selected]
            draw.text(
                (20, 62),
                f"{self.selected + 1}/{len(self.font_paths)}  {font_path.stem}",
                font=body_font,
                fill=0,
            )
            preview_font = ImageFont.truetype(font_path, 20)
            draw.text(
                (20, 100),
                "The quick brown fox jumps over the lazy dog.",
                font=preview_font,
                fill=0,
            )

        footer_y = self.display.width - 36
        draw.line((15, footer_y - 8, self.display.height - 15, footer_y - 8), fill=0)
        draw.text((20, footer_y), "Left/Right: preview   Select: apply", font=body_font, fill=0)
        draw.text((20, footer_y + 17), "Up/Down: cancel", font=body_font, fill=0)
        self.display.refresh()

    def handle_input(self, event):
        if event in (Event.UP, Event.DOWN):
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)
            return

        if not self.font_paths:
            return
        if event == Event.LEFT:
            self.selected = (self.selected - 1) % len(self.font_paths)
        elif event == Event.RIGHT:
            self.selected = (self.selected + 1) % len(self.font_paths)
        elif event == Event.SELECT:
            self.display.set_font_path(self.font_paths[self.selected])
            if self.app and getattr(self.app, "book_reader", None):
                self.app.book_reader.set_display(self.display)
            from app.screens.settings_menu import SettingsScreen
            self.ui.show(SettingsScreen)
            return
        else:
            return
        self.show()
