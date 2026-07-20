import time
import board
from adafruit_seesaw.seesaw import Seesaw

ss = Seesaw(board.I2C(), addr=0x49)

while True:
    try:
        print(hex(ss.get_version()))
    except Exception as e:
        print(e)

    time.sleep(0.1)