from PIL import Image
import sys

LIBDIR = "/home/viaod/e-Paper/E-paper_Separate_Program/3in7_e-Paper_G/RaspberryPi_JetsonNano/python/lib"

if LIBDIR not in sys.path:
    sys.path.append(LIBDIR)

from lib.waveshare_epd import epd3in7g


class Display:

    def __init__(self):

        self.epd = epd3in7g.EPD()

        self.epd.init()
        self.epd.Clear()

    def show_image(self, filename):

        image = Image.open(filename)

        # Resize to match the display
        image = image.resize(
            (self.epd.width, self.epd.height)
        )

        # Rotate image 90 degrees
        image = image.rotate(90)

        self.epd.display(
            self.epd.getbuffer(image)
        )

    def redraw(self, screen):

        image = Image.new(
            "1",
            (self.epd.width, self.epd.height),
            255
        )

        self.epd.display(
            self.epd.getbuffer(image)
        )

    def sleep(self):

        self.epd.sleep()