import time

from encoder import Encoder


encoder = Encoder()
encoder.initialise()

while True:
    encoder.update()
    time.sleep(0.05)
