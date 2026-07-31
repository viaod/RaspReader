from flask import Flask
from werkzeug.serving import make_server
import threading

from app.web.routes import register_routes


class WebServer:

    def __init__(
        self,
        library,
        host="0.0.0.0",
        port=8080
    ):
        self.host = host
        self.port = port
        self.library = library

        self.app = Flask(__name__)

        register_routes(
            self.app,
            self.library
        )

        self.server = None
        self.thread = None


    def start(self):

        if self.server is not None:
            return

        self.server = make_server(
            self.host,
            self.port,
            self.app
        )

        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )

        self.thread.start()


    def stop(self):

        if self.server is None:
            return

        self.server.shutdown()

        if self.thread is not None:
            self.thread.join()

        self.server = None
        self.thread = None