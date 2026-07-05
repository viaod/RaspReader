from PIL import Image
import sys

LIBDIR = "/home/viaod/e-Paper/E-paper_Separate_Program/3in7_e-Paper_G/RaspberryPi_JetsonNano/python/lib"

if LIBDIR not in sys.path:
    sys.path.append(LIBDIR)

from waveshare_epd import epd3in7g


class Display:

    def __init__(self):

        self.epd = epd3in7g.EPD()

        self.epd.init()
        self.epd.Clear()

    def show_image(self, filename):

        image = Image.open(filename)

        image = image.resize(
            (self.epd.width, self.epd.height)
        )

        self.epd.display(
            self.epd.getbuffer(image)
        )

    def sleep(self):
        self.epd.sleep()