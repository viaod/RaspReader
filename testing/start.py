#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

HOME = 0
MENU = 1

MENU_ITEMS = [
    "Library",
    "Continue Reading",
    "Settings",
    "Shutdown"
]

page = HOME
menu_index = 0

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("Initializing display...")

epd = epd3in7g.EPD()
epd.init()
epd.Clear()

font_title = ImageFont.load_default()
font = ImageFont.load_default()

# ------------------------------------------------------------
# Encoder
# ------------------------------------------------------------

print("Initializing encoder...")

i2c = board.I2C()

ss = seesaw.Seesaw(i2c, addr=0x49)

product = (ss.get_version() >> 16) & 0xFFFF
print("Found product:", product)

for pin in [1, 2, 3, 4, 5]:
    ss.pin_mode(pin, ss.INPUT_PULLUP)

select = digitalio.DigitalIO(ss, 1)
up = digitalio.DigitalIO(ss, 2)
left = digitalio.DigitalIO(ss, 3)
down = digitalio.DigitalIO(ss, 4)
right = digitalio.DigitalIO(ss, 5)

buttons = [select, up, left, down, right]
button_names = ["Select", "Up", "Left", "Down", "Right"]
button_state = [False] * 5

encoder = rotaryio.IncrementalEncoder(ss)
last_position = encoder.position


# ------------------------------------------------------------
# Draw Screen
# ------------------------------------------------------------

def redraw():

    image = Image.new("1", (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    if page == HOME:

        draw.text((150, 40), "RaspReader", font=font_title, fill=0)

        draw.line((70, 70, 340, 70), fill=0)

        draw.text((140, 120), "Press Select", font=font, fill=0)

    elif page == MENU:

        draw.text((20, 20), "RaspReader", font=font_title, fill=0)

        draw.line((20, 45, 390, 45), fill=0)

        y = 70

        for i, item in enumerate(MENU_ITEMS):

            if i == menu_index:
                draw.text((20, y), "> " + item, font=font, fill=0)
            else:
                draw.text((40, y), item, font=font, fill=0)

            y += 35

    epd.display(epd.getbuffer(image))


# Draw first screen
redraw()

print("Ready.")

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------

try:

    while True:

        # ----------------------------
        # Rotary Encoder
        # ----------------------------

        position = encoder.position

        if page == MENU and position != last_position:

            last_position = position

            menu_index = position % len(MENU_ITEMS)

            redraw()

        # ----------------------------
        # Buttons
        # ----------------------------

        for i in range(len(buttons)):

            pressed = not buttons[i].value

            if pressed and not button_state[i]:

                button_state[i] = True

                name = button_names[i]

                print(name)

                if name == "Select":

                    if page == HOME:
                        page = MENU
                        redraw()

                    else:
                        print("Selected:", MENU_ITEMS[menu_index])

                elif name == "Left":

                    if page == MENU:
                        page = HOME
                        redraw()

            elif not pressed and button_state[i]:

                button_state[i] = False

        time.sleep(0.02)

except KeyboardInterrupt:

    print("Closing display...")

    epd.init()
    epd.Clear()
    epd.sleep()
