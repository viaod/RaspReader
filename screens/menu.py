#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

from PIL import Image, ImageDraw, ImageFont

from screens.screen import Screen


MENU_ITEMS = [
    "Library",
    "Continue",
    "Settings",
    "Shutdown",
]


class MenuScreen(Screen):

    def __init__(self, display):

        super().__init__(display)

        self.selected = 0

        self.font = ImageFont.load_default()
        self.title_font = ImageFont.load_default()

    # -------------------------------------------------
    # Draw Screen
    # -------------------------------------------------

    def draw(self):

        image = Image.new(
            "1",
            (self.display.epd.width, self.display.epd.height),
            255,
        )

        draw = ImageDraw.Draw(image)

        #
        # Title
        #

        draw.text(
            (15, 15),
            "RaspReader",
            font=self.title_font,
            fill=0,
        )

        draw.line((15, 38, 400, 38), fill=0)

        #
        # Menu Items
        #

        y = 60

        for i, item in enumerate(MENU_ITEMS):

            if i == self.selected:

                draw.rectangle(
                    (15, y - 2, 220, y + 18),
                    outline=0,
                    width=2,
                )

            draw.text(
                (25, y),
                item,
                font=self.font,
                fill=0,
            )

            y += 35

        #
        # Footer
        #

        wifi = self.get_wifi_status()
        ip = self.get_ip()

        draw.line((0, 215, 415, 215), fill=0)

        draw.text(
            (10, 222),
            wifi,
            font=self.font,
            fill=0,
        )

        w = draw.textlength(ip, font=self.font)

        draw.text(
            (415 - w - 10, 222),
            ip,
            font=self.font,
            fill=0,
        )

        self.display.show(image)

    # -------------------------------------------------
    # Handle Encoder Events
    # -------------------------------------------------

    def handle_input(self, event):

        if event == "clockwise":

            self.selected = (self.selected + 1) % len(MENU_ITEMS)
            return True

        if event == "counter_clockwise":

            self.selected = (self.selected - 1) % len(MENU_ITEMS)
            return True

        if event == "select":

            return MENU_ITEMS[self.selected]

        return None

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def get_wifi_status(self):

        try:

            result = subprocess.check_output(
                ["cat", "/sys/class/net/wlan0/operstate"],
                text=True,
            ).strip()

            if result == "up":
                return "WiFi [ON]"

            return "WiFi [OFF]"

        except Exception:

            return "WiFi ?"

    def get_ip(self):

        try:

            ip = subprocess.check_output(
                ["hostname", "-I"],
                text=True,
            ).split()

            if ip:
                return ip[0]

        except Exception:
            pass

        return "No IP"