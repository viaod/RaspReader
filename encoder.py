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
        self.listeners = []
        self.last_position = 0
        self.rotation = 0

    def initialise(self):
        print("Initializing encoder...")

        i2c = board.I2C()
        self.ss = seesaw.Seesaw(i2c, addr=0x49)

        product = (self.ss.get_version() >> 16) & 0xFFFF
        print(f"Found product: {product}")
        if product != 5740:
            print("Wrong firmware loaded? Expected 5740")

        self.ss.pin_mode(1, self.ss.INPUT_PULLUP)
        self.ss.pin_mode(2, self.ss.INPUT_PULLUP)
        self.ss.pin_mode(3, self.ss.INPUT_PULLUP)
        self.ss.pin_mode(4, self.ss.INPUT_PULLUP)
        self.ss.pin_mode(5, self.ss.INPUT_PULLUP)

        self.buttons = [
            digitalio.DigitalIO(self.ss, 1),
            digitalio.DigitalIO(self.ss, 2),
            digitalio.DigitalIO(self.ss, 3),
            digitalio.DigitalIO(self.ss, 4),
            digitalio.DigitalIO(self.ss, 5),
        ]
        self.button_states = [False] * len(self.buttons)

        self.encoder = rotaryio.IncrementalEncoder(self.ss)
        self.last_position = self.encoder.position

    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def _notify(self, event):
        for listener in self.listeners:
            listener(event)

    def update(self):
        self.rotation = 0
        position = self.encoder.position

        if position > self.last_position:
            self.rotation = 1
            self._notify("clockwise")
        elif position < self.last_position:
            self.rotation = -1
            self._notify("counter_clockwise")

        self.last_position = position

        button = self.button_pressed()
        if button is not None:
            self._notify(button)

    def get_rotation(self):
        return self.rotation

    def button_pressed(self):
        for i, button in enumerate(self.buttons):
            pressed = not button.value
            if pressed and not self.button_states[i]:
                self.button_states[i] = True
                return self.BUTTON_NAMES[i]
            if not pressed and self.button_states[i]:
                self.button_states[i] = False
        return None