import board
from adafruit_seesaw.seesaw import Seesaw

i2c = board.I2C()
ss = Seesaw(i2c, addr=0x49)

print("Version:", hex(ss.get_version()))
print("Options:", hex(ss.get_options()))