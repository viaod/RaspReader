
import time

from app.encoder import Encoder
from app.events import Event


EVENT_NAMES = {
    Event.ROTATE_LEFT: "Rotate Left",
    Event.ROTATE_RIGHT: "Rotate Right",
    Event.UP: "UP",
    Event.DOWN: "DOWN",
    Event.LEFT: "LEFT",
    Event.RIGHT: "RIGHT",
    Event.SELECT: "SELECT",
}

def main():
    encoder = Encoder()

    try:
        encoder.initialize()
    except Exception as exc:
        print(f"Could not initialize encoder: {exc}")
        return

    def on_event(event):
        print(EVENT_NAMES.get(event, str(event)))

    encoder.add_listener(on_event)
    print("Waiting for encoder input...")

    try:
        while True:
            encoder.update()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting hardware test")


if __name__ == "__main__":
    main()