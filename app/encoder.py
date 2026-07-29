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
    
    MAX_VALID_DELTA = 1
    
    def __init__(self):
        self.ss = None
        self.encoder = None
        self.buttons = []
        self.button_states = []
        self.listeners = []
        self.last_position = 0
        self.rotation = 0
        self._last_emitted_position = None
        self.button_press_counts = [0] * 5
        self.encoder_out_of_sync = False
        
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
        delta = position - self.last_position

        # Normal encoder movement
        if delta == 1:
            if self.encoder_out_of_sync:
                logger.debug(f"Encoder resynchronised at {position}")
                self.encoder_out_of_sync = False
            else:
                self.rotation = 1
                self._notify(Event.ROTATE_RIGHT)

            self.last_position = position

        elif delta == -1:
            if self.encoder_out_of_sync:
                logger.debug(f"Encoder resynchronised at {position}")
                self.encoder_out_of_sync = False
            else:
                self.rotation = -1
                self._notify(Event.ROTATE_LEFT)

            self.last_position = position

        elif delta == 0:
            pass
        
        # Ignore obviously bogus encoder values
        else:
            ...
            # logger.debug(
            #     f"Ignored bogus encoder position {position} "
            #     f"(delta={delta}, last={self.last_position})"
            # )

        button = self.button_pressed()
        if button is not None:
            self._notify(button)
            
    def get_rotation(self):
        return self.rotation
    
    def button_pressed(self):
        for i, button in enumerate(self.buttons):
            pressed = not button.value

            if pressed:
                self.button_press_counts[i] += 1
            else:
                self.button_press_counts[i] = 0
                self.button_states[i] = False

            # Require 2 consecutive reads before treating as a press
            if (
                self.button_press_counts[i] >= 2
                and not self.button_states[i]
            ):
                self.button_states[i] = True
                return self.BUTTON_EVENTS[self.BUTTON_NAMES[i]]

        return None