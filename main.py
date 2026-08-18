import time

from app.core.events import Event
from app.core.logger import Logger
from app.core.ui import UI
from app.screens.home import HomeScreen
from app.library.library_manager import LibraryManager
from app.web.server import WebServer
from app.reader.book_reader import BookReader


logger = Logger("App")


class App:
    def __init__(self):
        self.display = None
        self.encoder = None
        self.ui = None
        self.library = None
        self.web_server = None
        self.selected_book = None
        self.running = True
        
    def initialize(self):
        
        self.library = LibraryManager()
        self.book_reader = BookReader(self.library)
        
        self.web_server = WebServer(
            self.library
        )
        
        try:
            from app.hardware.display import Display
            self.display = Display()
            
            self.book_reader.set_display(self.display)
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
        
        self.ui = UI(
            self.display,
            app=self
        )
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

        if self.book_reader:
            self.book_reader.save_position()

        if self.display:
            # Ensure a full clear and put the display to sleep so it
            # doesn't retain an image after the app exits.
            try:
                self.display.clear(force_full=True)
            except Exception:
                # best-effort: still try to sleep the display
                pass
            try:
                self.display.sleep()
            except Exception:
                pass
        logger.info("App shutdown")


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()