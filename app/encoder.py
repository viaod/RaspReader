#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import board
from adafruit_seesaw import seesaw, digitalio, rotaryio

from app.events import Event
from app.logger import Logger

logger = Logger("Encoder")

class Encoder:
    
    BUTTON_NAMES = [
        "select",
        "up",
        "left",
        "down",
        "right",
    ]

    BUTTON_EVENTS = {
        "select": Event.SELECT,
        "up": Event.UP,
        "left": Event.LEFT,
        "down": Event.DOWN,
        "right": Event.RIGHT,
    }
    
    def __init__(self):
        self.ss = None
        self.encoder = None
        self.buttons = []
        self.button_states = []
        self.listeners = []
        self.last_position = 0
        self.rotation = 0
        self._last_emitted_position = None
        
    def initialize(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.ss = seesaw.Seesaw(i2c, addr=0x49)
        
        # Set up the rotary encoder
        self.encoder = rotaryio.IncrementalEncoder(self.ss)
        self.last_position = self.encoder.position
        self._last_emitted_position = self.last_position
        
        # Set up the buttons
        input_pullup = getattr(self.ss, "INPUT_PULLUP", None)
        if input_pullup is None:
            input_pullup = getattr(seesaw, "INPUT_PULLUP", None)
            if input_pullup is None:
                raise AttributeError("Your installed seesaw package does not expose INPUT_PULLUP")

        for pin in range(1, 6):
            self.ss.pin_mode(pin, input_pullup)
            button = digitalio.DigitalIO(self.ss, pin)
            self.buttons.append(button)
            self.button_states.append(False)  # Initialize button states to False (not pressed)
        
        logger.info("Encoder initialized")
        
    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)
            logger.info(f"Listener {listener} added")

    def _notify(self, event):
        for listener in self.listeners:
            listener(event)
            logger.info(f"Notified listener {listener} with event: {event}")
            
    def update(self):
        self.rotation = 0
        position = self.encoder.position

        if position != self.last_position:
            delta = position - self.last_position

            if delta > 0:
                self.rotation = 1
                self._notify(Event.ROTATE_RIGHT)
            elif delta < 0:
                self.rotation = -1
                self._notify(Event.ROTATE_LEFT)

            self.last_position = position
        else:
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
                return self.BUTTON_EVENTS[self.BUTTON_NAMES[i]]
            if not pressed and self.button_states[i]:
                self.button_states[i] = False
        return None