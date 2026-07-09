# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C ANO rotary encoder simple test example."""

import board

from adafruit_seesaw import digitalio, rotaryio, seesaw

I2C_ADDRESSES = (0x49, 0x36, 0x30)


def connect_seesaw(i2c):
    last_error = None

    for addr in I2C_ADDRESSES:
        try:
            ss = seesaw.Seesaw(i2c, addr=addr)
            product = (ss.get_version() >> 16) & 0xFFFF
            print(f"Found seesaw device at 0x{addr:02x}: product {product}")

            if product == 5740:
                return ss

        except Exception as exc:
            last_error = exc
            print(f"No response at 0x{addr:02x}: {exc}")

    raise RuntimeError(
        "Could not find a compatible seesaw encoder. Check wiring, power, and I2C address. "
        "Run `i2cdetect -y 1` on the Pi and confirm the device appears at 0x49, 0x36, or 0x30."
    ) from last_error


i2c = board.I2C()
seesaw_device = connect_seesaw(i2c)

seesaw_product = (seesaw_device.get_version() >> 16) & 0xFFFF
print(f"Found product {seesaw_product}")
if seesaw_product != 5740:
    print("Wrong firmware loaded? Expected 5740")

seesaw_device.pin_mode(1, seesaw_device.INPUT_PULLUP)
seesaw_device.pin_mode(2, seesaw_device.INPUT_PULLUP)
seesaw_device.pin_mode(3, seesaw_device.INPUT_PULLUP)
seesaw_device.pin_mode(4, seesaw_device.INPUT_PULLUP)
seesaw_device.pin_mode(5, seesaw_device.INPUT_PULLUP)

select = digitalio.DigitalIO(seesaw_device, 1)
select_held = False
up = digitalio.DigitalIO(seesaw_device, 2)
up_held = False
left = digitalio.DigitalIO(seesaw_device, 3)
left_held = False
down = digitalio.DigitalIO(seesaw_device, 4)
down_held = False
right = digitalio.DigitalIO(seesaw_device, 5)
right_held = False

encoder = rotaryio.IncrementalEncoder(seesaw_device)
last_position = None

buttons = [select, up, left, down, right]
button_names = ["Select", "Up", "Left", "Down", "Right"]
button_states = [select_held, up_held, left_held, down_held, right_held]

while True:
    position = encoder.position

    if position != last_position:
        last_position = position
        print(f"Position: {position}")

    for b in range(5):
        if not buttons[b].value and button_states[b] is False:
            button_states[b] = True
            print(f"{button_names[b]} button pressed")

        if buttons[b].value and button_states[b] is True:
            button_states[b] = False
            print(f"{button_names[b]} button released")