#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
from functools import lru_cache

picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "pic",
)

libdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "lib",
)

if os.path.exists(libdir):
    sys.path.insert(0, libdir)

from lib.waveshare_epd import epd3in7
from PIL import Image, ImageDraw, ImageFont

from app.core.logger import Logger
from app.core.config import FONT_PATH, TEXT_SCALE

logger = Logger("Display")


class Display:

    def __init__(self):
        self.epd = epd3in7.EPD()

        # Provide backwards-compatible color constants expected by
        # other code. Some Waveshare drivers expose GRAY1..GRAY4
        # instead of WHITE/BLACK.
        if not hasattr(self.epd, "WHITE"):
            self.epd.WHITE = getattr(self.epd, "GRAY1", 0xFF)
        if not hasattr(self.epd, "BLACK"):
            self.epd.BLACK = getattr(self.epd, "GRAY4", 0x00)

        # Initialize display driver. Different Waveshare drivers
        # have different signatures for `init()` and `Clear()`; try
        # the no-arg form first, fall back to common signatures.
        try:
            self.epd.init()
        except TypeError:
            try:
                # many drivers accept a numeric mode (0 or 1)
                self.epd.init(1)
            except Exception as e:
                logger.error(f"Display init failed: {e}")
                raise

        # Clear the display; some drivers require (color, mode)
        try:
            self.epd.Clear()
        except TypeError:
            try:
                # use 0xFF as the clear (white) color when driver expects it
                self.epd.Clear(0xFF, 1)
            except Exception:
                # non-fatal: continue even if clear failed
                logger.warning("Display Clear() not supported with default args; continuing")

        # driver doesn't support a separate fast refresh mode

        self.width = self.epd.width
        self.height = self.epd.height

        logger.info(f"Display size: {self.width}x{self.height}")

        # IMPORTANT:
        # Use grayscale ('L') canvas because this driver expects
        # 1- or 4-bit grayscale buffers. Creating an 'L' image
        # avoids color/alpha conversion surprises that produced
        # a grey-looking background previously.
        self.image = Image.new(
            "L",
            (self.height, self.width),
            int(self.epd.WHITE),
        )

        self.draw = ImageDraw.Draw(self.image)

        logger.info("Display initialized")

    def show(self, image):
        # Choose the appropriate driver API based on what's available.
        try:
            # Normalize canvas to driver-expected orientation: many Waveshare
            # examples use (height, width) for horizontal buffers.
            img = image
            if img.size != (self.height, self.width):
                img = img.resize((self.height, self.width))

            # Prefer 4-gray APIs when present
            if hasattr(self.epd, "display_4Gray") and hasattr(self.epd, "getbuffer_4Gray"):
                buf = self.epd.getbuffer_4Gray(img.convert("L"))
                self.epd.display_4Gray(buf)
            # Fallback to 1-gray APIs
            elif hasattr(self.epd, "display_1Gray") and hasattr(self.epd, "getbuffer"):
                buf = self.epd.getbuffer(img)
                try:
                    self.epd.display_1Gray(buf)
                except AttributeError:
                    # some drivers expose a generic 'display' method
                    if hasattr(self.epd, "display"):
                        self.epd.display(buf)
                    else:
                        raise
            else:
                # Last-resort: try a generic display call with a raw buffer
                buf = self.epd.getbuffer(img)
                if hasattr(self.epd, "display"):
                    self.epd.display(buf)
                else:
                    raise RuntimeError("No compatible display method found on epd driver")

            logger.info("Display updated")
        except Exception as e:
            logger.error(f"Failed to update display: {e}")
            raise

    def show_image(self, image_path):
        image = Image.open(image_path)

        # Convert to grayscale to match the canvas and driver expectations.
        image = image.convert("L")

        # Let `show()` handle orientation; resize to the canvas size.
        image = image.resize((self.height, self.width))

        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.show(self.image)

        logger.info(f"Displayed image: {image_path}")

    def clear_image(self):
        self.draw.rectangle(
            (
                0,
                0,
                self.height,
                self.width,
            ),
            fill=self.epd.WHITE,
        )

    def draw_text(
        self,
        text,
        position,
        font=None,
        fill=None,
    ):
        if font is None:
            font = ImageFont.load_default()

        if fill is None:
            fill = self.epd.BLACK

        self.draw.text(
            position,
            text,
            font=font,
            fill=fill,
        )

    def draw_rectangle(
        self,
        xy,
        fill=None,
    ):
        if fill is None:
            fill = self.epd.BLACK

        self.draw.rectangle(
            xy,
            fill=fill,
        )

    @staticmethod
    def _font_paths():
        """Return fonts available on both the Pi and local development PCs."""
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        candidates = [
            FONT_PATH,
            os.path.join(project_dir, "assets", "fonts", "Font.ttc"),
            os.path.join(project_dir, "assets", "fonts", "DejaVuSans.ttf"),
            os.path.join(picdir, "Font.ttc"),
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
        return [path for path in candidates if path and os.path.isfile(path)]

    @lru_cache(maxsize=32)
    def get_font(self, size=18):
        """Load a scalable font, applying the application-wide TEXT_SCALE."""
        scaled_size = max(1, round(size * TEXT_SCALE))
        for font_path in self._font_paths():
            try:
                return ImageFont.truetype(font_path, scaled_size)
            except OSError:
                logger.warning("Unable to load font: %s", font_path)
        logger.warning("No scalable font found; using Pillow's fixed-size fallback")
        return ImageFont.load_default()

    def refresh(self):
        self.show(self.image)

    def clear(self, force_full: bool = False):
        """Clear the display. If `force_full` is True, attempt a full
        clear sequence (init full mode, clear with mode=0) which matches
        the Waveshare example scripts.
        """
        # If requested, try to init full-update mode first.
        if force_full:
            try:
                # many driver variants accept a numeric mode for init
                try:
                    self.epd.init(0)
                except TypeError:
                    # some drivers only accept no-arg init; try calling
                    # no-arg init then assume Clear(mode=0) will work.
                    self.epd.init()
            except Exception as e:
                logger.warning(f"Failed to init full-clear mode: {e}")

            # Try the Waveshare-style full clear (color 0xFF, mode 0)
            try:
                self.epd.Clear(0xFF, 0)
                logger.info("Display full-clear completed")
                return
            except TypeError:
                # driver doesn't accept (color, mode) signature; fall back
                # to regular Clear below
                pass
            except Exception as e:
                logger.warning(f"Full Clear() attempt failed: {e}")

        # Normal clear path: try no-arg Clear(), otherwise try Clear(color, mode)
        try:
            self.epd.Clear()
        except TypeError:
            try:
                self.epd.Clear(0xFF, 1)
            except Exception as e:
                logger.error(f"Display clear failed: {e}")
                return

        logger.info("Display cleared")

    def sleep(self):
        self.epd.sleep()
        logger.info("Display put to sleep")

    def use_fast_mode(self):
        # Removed: this driver does not support a fast/partial init API.
        logger.debug("use_fast_mode called but not supported; no-op")

    def use_full_mode(self):
        # Removed: no-op for drivers without fast/full mode support.
        logger.debug("use_full_mode called but not supported; no-op")
