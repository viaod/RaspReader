#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Display helper functions 

import sys
import time

# ------------------------------------------------------------
# Waveshare Library
# ------------------------------------------------------------
LIBDIR = "/home/viaod/e-Paper/E-paper_Separate_Program/3in7_e-Paper_G/RaspberryPi_JetsonNano/python/lib"

if LIBDIR not in sys.path:
    sys.path.append(LIBDIR)

from waveshare_epd import epd3in7g

# ------------------------------------------------------------
# Encoder
# ------------------------------------------------------------
import board
from adafruit_seesaw import seesaw, digitalio, rotaryio

# ------------------------------------------------------------
# Pillow
# ------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont



def initialise ():
    print("Initializing display...")

    epd = epd3in7g.EPD()
    epd.init()
    epd.Clear()

    font_title = ImageFont.load_default()
    font = ImageFont.load_default()
    
def draw():
    ...
def redraw():
    ...
