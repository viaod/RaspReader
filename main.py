import time

from app.core.events import Event
from app.core.logger import Logger
from app.core.ui import UI
from app.screens.home import HomeScreen

logger = Logger("App")


class App:
    def __init__(self):
        self.display = None
        self.encoder = None
        self.ui = None
        self.running = True

    def initialize(self):
        try:
            from app.hardware.display import Display
            self.display = Display()
        except Exception as exc:
            logger.warning(f"Display unavailable: {exc}")
            self.display = None

        try:
            from app.hardware.encoder import Encoder
            self.encoder = Encoder()
            self.encoder.initialize()
            self.encoder.add_listener(self.handle_input)
        except Exception as exc:
            logger.warning(f"Encoder unavailable: {exc}")
            self.encoder = None

        self.ui = UI(self.display)
        self.ui.show(HomeScreen)
        logger.info("App initialized")

    def handle_input(self, event):
        if self.ui is not None:
            self.ui.handle_input(event)

    def run(self):
        self.initialize()

        try:
            while self.running:
                if self.encoder is not None:
                    self.encoder.update()
                time.sleep(0.01)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            self.shutdown()

    def shutdown(self):
        self.running = False
        if self.display is not None:
            self.display.clear()
        logger.info("App shutdown")


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()