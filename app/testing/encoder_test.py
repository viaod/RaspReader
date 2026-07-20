# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C ANO rotary encoder simple test example."""

import board

from adafruit_seesaw import digitalio, rotaryio, seesaw

i2c = board.I2C()
seesaw = seesaw.Seesaw(i2c, addr=0x49)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print(f"Found product {seesaw_product}")
if seesaw_product != 5740:
    print("Wrong firmware loaded? Expected 5740")

for pin in range(1, 6):
    seesaw.pin_mode(pin, seesaw.INPUT_PULLUP)

buttons = [
    digitalio.DigitalIO(seesaw, 1),  # Select
    digitalio.DigitalIO(seesaw, 2),  # Up
    digitalio.DigitalIO(seesaw, 3),  # Left
    digitalio.DigitalIO(seesaw, 4),  # Down
    digitalio.DigitalIO(seesaw, 5),  # Right
]

button_names = ["Select", "Up", "Left", "Down", "Right"]
button_states = [False] * 5

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = encoder.position

while True:
    position = encoder.position
    delta = position - last_position

    # Ignore obviously bogus jumps
    if abs(delta) <= 2:
        if delta != 0:
            print(f"Position: {position}")
            last_position = position
    else:
        print(f"Ignored bogus position: {position} (delta={delta})")

    for b in range(5):
        pressed = not buttons[b].value

        if pressed and not button_states[b]:
            button_states[b] = True
            print(f"{button_names[b]} button pressed")

        elif not pressed and button_states[b]:
            button_states[b] = False
            print(f"{button_names[b]} button released")