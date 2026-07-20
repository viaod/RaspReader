import time
import board
from adafruit_seesaw.seesaw import Seesaw

ss = Seesaw(board.I2C(), addr=0x49)

while True:
    try:
        print(ss.encoder_position())
    except Exception as e:
        print(e)

    time.sleep(0.1)