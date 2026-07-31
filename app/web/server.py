from flask import Flask
from werkzeug.serving import make_server
import threading

from app.web.routes import register_routes


class WebServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port

        self.app = Flask(__name__)
        register_routes(self.app)

        self.server = None
        self.thread = None

    def start(self):
        if self.server is not None:
            return

        self.server = make_server(self.host, self.port, self.app)
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )
        self.thread.start()

    def stop(self):
        if self.server is None:
            return

        self.server.shutdown()
        self.thread.join()

        self.server = None
        self.thread = None


def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080)