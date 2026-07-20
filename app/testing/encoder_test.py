import time
import board
from adafruit_seesaw import seesaw, rotaryio

i2c = board.I2C()
ss = seesaw.Seesaw(i2c, addr=0x49)

encoder = rotaryio.IncrementalEncoder(ss)

last = encoder.position

while True:
    pos = encoder.position
    if pos != last:
        print(pos)
        last = pos
    time.sleep(0.01)