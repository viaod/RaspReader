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
        print("=== upload route ===")

        file = request.files.get("book")

        print("file:", file)
        print("filename:", file.filename if file else None)

        if file is None or file.filename == "":
            print("No file selected")
            return render_template(
                "upload.html",
                books=library.get_books(),
                error="Please choose a book."
            )

        try:
            upload_book(file, library)
            print("Upload succeeded")
        except Exception as e:
            print("Caught:", type(e).__name__, e)
            return render_template(
                "upload.html",
                books=library.get_books(),
                error=str(e)
            )

        print("Redirecting")
        return redirect("/")