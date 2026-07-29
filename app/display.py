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

from waveshare_epd import epd3in7g
from PIL import Image, ImageDraw, ImageFont

from app.logger import Logger

logger = Logger("Display")


class Display:

    def __init__(self):
        self.epd = epd3in7g.EPD()

        self.epd.init()
        self.epd.Clear()

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
        self.epd.display(
            self.epd.getbuffer(image)
        )
        logger.info("Display updated")

    def show_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        # Match the canvas size exactly
        image = image.resize(
            (self.height, self.width)
        )

        self.show(image)

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
        self.epd.Clear()
        logger.info("Display cleared")

    def sleep(self):
        self.epd.sleep()
        logger.info("Display put to sleep")