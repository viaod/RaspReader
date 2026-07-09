#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encoder driver for the Adafruit ANO Navigation Encoder.
"""

import board
from adafruit_seesaw import seesaw, digitalio, rotaryio


class Encoder:

    BUTTON_NAMES = [
        "select",
        "up",
        "left",
        "down",
        "right",
    ]

    def __init__(self):

        self.ss = None
        self.encoder = None

        self.buttons = []
        self.button_states = []

        self.last_position = 0
        self.rotation = 0

    def initialise(self):

        print("Initializing encoder...")

        i2c = board.I2C()

        self.ss = seesaw.Seesaw(i2c, addr=0x49)

        product = (self.ss.get_version() >> 16) & 0xFFFF
        print(f"Found product: {product}")

        for pin in [1, 2, 3, 4, 5]:
            self.ss.pin_mode(pin, self.ss.INPUT_PULLUP)

        self.buttons = [
            digitalio.DigitalIO(self.ss, 1),  # Select
            digitalio.DigitalIO(self.ss, 2),  # Up
            digitalio.DigitalIO(self.ss, 3),  # Left
            digitalio.DigitalIO(self.ss, 4),  # Down
            digitalio.DigitalIO(self.ss, 5),  # Right
        ]

        self.button_states = [False] * len(self.buttons)

        self.encoder = rotaryio.IncrementalEncoder(self.ss)
        self.last_position = self.encoder.position

    def update(self):
        """
        Call once every loop.
        """

        self.rotation = 0

        position = self.encoder.position

        if position > self.last_position:
            self.rotation = 1

        elif position < self.last_position:
            self.rotation = -1

        self.last_position = position

    def get_rotation(self):
        """
        Returns:
            -1 = anticlockwise
             0 = no movement
             1 = clockwise
        """

        return self.rotation

    def button_pressed(self):
        """
        Returns the name of the button that was JUST pressed.

        Returns:
            "select"
            "up"
            "left"
            "down"
            "right"
            None
        """

        for i, button in enumerate(self.buttons):

            pressed = not button.value

            if pressed and not self.button_states[i]:
                self.button_states[i] = True
                return self.BUTTON_NAMES[i]

            elif not pressed and self.button_states[i]:
                self.button_states[i] = False

        return None