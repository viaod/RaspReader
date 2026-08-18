#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

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

logger = Logger("Display")


class Display:

    def __init__(self):
        self.epd = epd3in7.EPD()

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
                self.epd.Clear(0, 1)
            except Exception:
                # non-fatal: continue even if clear failed
                logger.warning("Display Clear() not supported with default args; continuing")

        # flag for switching between full and fast refresh
        self.fast_mode = False

        self.width = self.epd.width
        self.height = self.epd.height

        logger.info(f"Display size: {self.width}x{self.height}")

        # IMPORTANT:
        # The official Waveshare driver expects an RGB image with the
        # dimensions (height, width), not (width, height).
        self.image = Image.new(
            "RGB",
            (self.height, self.width),
            self.epd.WHITE,
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

        # Let `show()` handle conversion and orientation; just resize.
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

    def get_font(self, size=18):
        try:
            return ImageFont.truetype(
                os.path.join(picdir, "Font.ttc"),
                size,
            )
        except Exception:
            return ImageFont.load_default()

    def refresh(self):
        self.show(self.image)

    def clear(self):
        # Some drivers require arguments for Clear(); try both.
        try:
            self.epd.Clear()
        except TypeError:
            try:
                self.epd.Clear(0, 1)
            except Exception as e:
                logger.error(f"Display clear failed: {e}")
                return

        logger.info("Display cleared")

    def sleep(self):
        self.epd.sleep()
        logger.info("Display put to sleep")

    def use_fast_mode(self):
        # The currently-installed driver may not support a fast-init
        # API (init_Fast). Only call it when present; otherwise no-op.
        if not self.fast_mode:
            logger.info("Switching to fast refresh mode")
            if hasattr(self.epd, "init_Fast"):
                try:
                    self.epd.init_Fast()
                    self.fast_mode = True
                except Exception as e:
                    logger.warning(f"init_Fast failed: {e}; remaining in full mode")
            else:
                logger.debug("Driver has no init_Fast; fast mode skipped")

    def use_full_mode(self):
        if self.fast_mode:
            logger.info("Switching to full refresh mode")
            try:
                self.epd.init()
            except TypeError:
                try:
                    self.epd.init(1)
                except Exception as e:
                    logger.warning(f"full init failed: {e}")
            self.fast_mode = False
