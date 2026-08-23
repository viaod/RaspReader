#!/usr/bin/env python3
"""Standalone font preview for the e-reader display and encoder.

Run on the Raspberry Pi from the project root with:
    python3 -m app.testing.font_test

Use the encoder's Left and Right buttons to change the font.  Press Ctrl+C
in the terminal to clear the display and exit.
"""

import os
import time

from PIL import ImageFont

from app.core.events import Event
from app.hardware.display import Display
from app.hardware.encoder import Encoder


SAMPLE_SIZES = (12, 16, 20, 26)


class FontPreview:
    """Draw font samples and switch between installed font files."""

    def __init__(self, display):
        self.display = display
        self.font_paths = display._font_paths()
        self.selected_font = 0

    def _font_name(self):
        if not self.font_paths:
            return "Pillow default"
        return os.path.basename(self.font_paths[self.selected_font])

    def _load_font(self, size):
        if not self.font_paths:
            return ImageFont.load_default()
        return ImageFont.truetype(self.font_paths[self.selected_font], size)

    def show(self):
        draw = self.display.draw
        self.display.clear_image()

        title_font = self.display.get_font(18)
        body_font = self.display.get_font(12)
        title = "Font preview"
        draw.text((15, 15), title, font=title_font, fill=0)
        draw.line((15, 42, self.display.height - 15, 42), fill=0)

        position = "Pillow default" if not self.font_paths else (
            f"{self.selected_font + 1}/{len(self.font_paths)}"
        )
        draw.text((15, 50), f"{position}: {self._font_name()}", font=body_font, fill=0)

        y = 75
        for size in SAMPLE_SIZES:
            font = self._load_font(size)
            draw.text((20, y), f"{size}px  The quick brown fox", font=font, fill=0)
            y += size + 12

        draw.line((15, self.display.width - 42, self.display.height - 15, self.display.width - 42), fill=0)
        draw.text(
            (15, self.display.width - 32),
            "Left / Right: change font   Ctrl+C: exit",
            font=body_font,
            fill=0,
        )
        self.display.refresh()

    def handle_event(self, event):
        if not self.font_paths:
            return
        if event == Event.LEFT:
            self.selected_font = (self.selected_font - 1) % len(self.font_paths)
        elif event == Event.RIGHT:
            self.selected_font = (self.selected_font + 1) % len(self.font_paths)
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
