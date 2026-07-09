from pathlib import Path
from PIL import Image
import sys

PROJECT_ROOT = Path(__file__).resolve().parent

for candidate in (
    PROJECT_ROOT / "lib" / "e-Paper" / "lib",
    PROJECT_ROOT / "lib" / "e-Paper" / "python",
    PROJECT_ROOT / "lib" / "e-Paper" / "RaspberryPi_JetsonNano" / "python",
):
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

try:
    from waveshare_epd import epd3in7g
except ImportError as exc:
    raise ImportError(
        "Could not import the Waveshare e-paper library. "
        "Expected it under lib/e-Paper/lib or a matching path."
    ) from exc


class Display:

    def __init__(self):

        self.epd = epd3in7g.EPD()

        self.epd.init()
        self.epd.Clear()
        
    def show(self, image):
        """Display an existing PIL Image."""

        self.epd.display(
            self.epd.getbuffer(image)
        )

    def show_image(self, filename):

        image = Image.open(filename)

        # Waveshare 3.7" expects height x width orientation
        image = image.resize(
            (self.epd.height, self.epd.width)
        )

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