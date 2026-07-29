#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd3in7g
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from app.logger import Logger

logger = Logger("Display")

class Display:
    
    def __init__(self):
        self.epd = epd3in7g.EPD()
        self.epd.init()
        
        self.epd.Clear()
        
        self.width = self.epd.width
        self.height = self.epd.height
        
        self.image = Image.new('1', (self.width, self.height), 255) 
        self.draw = ImageDraw.Draw(self.image)
        
        logger.info("Display initialized")

    def show(self, image):
        self.epd.display(self.epd.getbuffer(image))
        logger.info("Display updated")
        
    def show_image(self, image_path):
        image = Image.open(image_path)
        self.show(image)
        logger.info(f"Displayed image: {image_path}")
        
    def draw_text(self, text, position, font=None, fill=0):
        if font is None:
            font = ImageFont.load_default()
        self.draw.text(position, text, font=font, fill=fill)
        logger.info(f"Drew text: '{text}' at position: {position}")
        
    def draw_rectangle(self, xy, fill=0):
        self.draw.rectangle(xy, fill=fill)
        logger.info(f"Drew rectangle at: {xy} with fill: {fill}")  
    
    def clear_image(self):
        self.image.paste(
            255,
            (0, 0, self.width, self.height),
        )

    def get_font(self, size=18):
        try:
            return ImageFont.truetype(
                os.path.join(picdir, "Font.ttc"),
                size,
            )
        except Exception:
            return ImageFont.load_default()    
        
    def clear(self):
        self.epd.Clear()
        logger.info("Display cleared")
    
    def refresh(self):
        self.show(self.image)
        logger.info("Display refreshed")
    
    def sleep(self):
        self.epd.sleep()
        logger.info("Display put to sleep")
        
