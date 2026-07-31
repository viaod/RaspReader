from flask import (
    render_template,
    request,
    redirect,
    flash,
)

from app.library.library_manager import LibraryManager
Logger
from app.web.upload import upload_book

library = LibraryManager()


def register_routes(app):

    @app.route("/")
    def index():

        return render_template(
            "upload.html",
            books=library.get_books(),
        )

    @app.route("/upload", methods=["POST"])
    def upload():
        file = request.files.get("book")

        if file is None or file.filename == "":
            return render_template(
                "upload.html",
                books=library.get_books(),
                error="Please choose a book."
            )

        try:
            upload_book(file, library)
        except ValueError as e:
            return render_template(
                "upload.html",
                books=library.get_books(),
                error=str(e)
            )

        return redirect("/")