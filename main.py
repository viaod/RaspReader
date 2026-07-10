import time

from app.events import Event
from app.logger import Logger
from app.ui import UI

logger = Logger("App")


class App:
    def __init__(self):
        self.display = None
        self.encoder = None
        self.ui = None
        self.running = True

    def initialize(self):
        try:
            from app.display import Display
            self.display = Display()
        except Exception as exc:
            logger.warning(f"Display unavailable: {exc}")
            self.display = None

        try:
            from app.encoder import Encoder
            self.encoder = Encoder()
            self.encoder.initialize()
            self.encoder.add_listener(self.handle_input)
        except Exception as exc:
            logger.warning(f"Encoder unavailable: {exc}")
            self.encoder = None

        self.ui = UI(self.display)
        self.ui.show_home()
        logger.info("App initialized")

    def handle_input(self, event):
        if event == Event.ROTATE_RIGHT:
            logger.info("Rotate right")
        elif event == Event.ROTATE_LEFT:
            logger.info("Rotate left")
        elif event == Event.UP:
            logger.info("Up button")
        elif event == Event.DOWN:
            logger.info("Down button")
        elif event == Event.LEFT:
            logger.info("Left button")
        elif event == Event.RIGHT:
            logger.info("Right button")
        elif event == Event.SELECT:
            logger.info("Select button")

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