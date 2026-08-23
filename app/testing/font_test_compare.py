#!/usr/bin/env python3
"""Standalone font preview for the e-reader display and encoder.

Run on the Raspberry Pi from the project root with:
    python3 -m app.testing.font_test

Use the encoder's Left and Right buttons to change the group of four fonts.
Press Ctrl+C in the terminal to clear the display and exit.
"""

import time
from pathlib import Path

from PIL import ImageFont

from app.core.events import Event
from app.hardware.display import Display
from app.hardware.encoder import Encoder


FONTS_PER_PAGE = 4
SAMPLE_TEXT = "The quick brown fox jumps over the lazy dog."


class FontPreview:
    """Draw four samples at once and switch between assets/fonts pages."""

    def __init__(self, display):
        self.display = display
        fonts_dir = Path(__file__).resolve().parents[2] / "assets" / "fonts"
        self.font_paths = sorted(
            path
            for extension in ("*.ttf", "*.otf", "*.ttc")
            for path in fonts_dir.glob(extension)
        )
        self.page = 0

    @property
    def page_count(self):
        return max(1, (len(self.font_paths) + FONTS_PER_PAGE - 1) // FONTS_PER_PAGE)

    def _load_font(self, font_path, size):
        return ImageFont.truetype(font_path, size)

    def show(self):
        draw = self.display.draw
        self.display.clear_image()

        title_font = self.display.get_font(18)
        body_font = self.display.get_font(12)
        title = "Font preview"
        draw.text((15, 15), title, font=title_font, fill=0)
        draw.line((15, 42, self.display.height - 15, 42), fill=0)

        draw.text(
            (15, 50),
            f"Fonts {self.page * FONTS_PER_PAGE + 1}-{min((self.page + 1) * FONTS_PER_PAGE, len(self.font_paths))} of {len(self.font_paths)}",
            font=body_font,
            fill=0,
        )

        start = self.page * FONTS_PER_PAGE
        for row, font_path in enumerate(self.font_paths[start:start + FONTS_PER_PAGE]):
            y = 70 + row * 42
            draw.text((20, y), font_path.stem, font=body_font, fill=0)
            draw.text((20, y + 13), SAMPLE_TEXT, font=self._load_font(font_path, 18), fill=0)

        draw.line((15, self.display.width - 42, self.display.height - 15, self.display.width - 42), fill=0)
        draw.text(
            (15, self.display.width - 32),
            f"Left / Right: page {self.page + 1}/{self.page_count}   Ctrl+C: exit",
            font=body_font,
            fill=0,
        )
        self.display.refresh()

    def handle_event(self, event):
        if event == Event.LEFT:
            self.page = (self.page - 1) % self.page_count
        elif event == Event.RIGHT:
            self.page = (self.page + 1) % self.page_count
        else:
            return
        self.show()


def main():
    display = Display()
    preview = FontPreview(display)
    encoder = Encoder()

    try:
        encoder.initialize()
    except Exception as exc:
        print(f"Could not initialize encoder: {exc}")
        return

    encoder.add_listener(preview.handle_event)
    preview.show()
    print("Font preview running. Use Left/Right; press Ctrl+C to exit.")

    try:
        while True:
            encoder.update()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting font preview")
    finally:
        display.clear_image()
        display.refresh()
        display.sleep()


if __name__ == "__main__":
    main()
