from flask import (
    render_template,
    request,
    redirect,
    flash,
)

from app.library.library_manager import LibraryManager
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
        except Exception as e:
            print(type(e), repr(e))   # Debug
            return render_template(
                "upload.html",
                books=library.get_books(),
                error=f"{type(e).__name__}: {e}"
            )

        return redirect("/")