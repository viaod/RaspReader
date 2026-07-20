import board
from adafruit_seesaw.seesaw import Seesaw

ss = Seesaw(board.I2C(), addr=0x49)

print(hex(ss.get_version()))

for i in range(20):
    try:
        print(i, ss.encoder_position())
    except Exception as e:
        print(i, e)