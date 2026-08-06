from pathlib import Path

from flask import (
    render_template,
    request,
    redirect,
)

from app.library.book_cache import BookCache
from app.library.progress import ProgressManager
from app.web.upload import upload_book


def register_routes(app, library):
    book_cache = BookCache()
    progress = ProgressManager()

    def get_book_from_filename(filename):
        safe_filename = Path(filename).name
        if safe_filename != filename:
            return None
        return library.get_book(safe_filename)

    @app.route("/")
    def index():
        return render_template(
            "upload.html",
            books=library.get_books(),
            error=request.args.get("error"),
            success=request.args.get("success"),
        )

    @app.route("/upload", methods=["POST"])
    def upload():
        file = request.files.get("book")

        if file is None or file.filename == "":
            return redirect("/?error=Please%20choose%20a%20book")

        try:
            upload_book(file, library)
        except ValueError as exc:
            return redirect(f"/?error={exc}")

        return redirect("/?success=Book%20uploaded%20successfully")

    @app.route("/books/<path:filename>/cache/delete", methods=["POST"])
    def delete_cache(filename):
        book = get_book_from_filename(filename)
        if book is None:
            return redirect("/?error=Book%20not%20found")

        if not book_cache.delete(book):
            return redirect("/?error=No%20cache%20exists%20for%20that%20book")

        return redirect("/?success=Book%20cache%20deleted")

    @app.route("/books/<path:filename>/delete", methods=["POST"])
    def delete_book(filename):
        book = get_book_from_filename(filename)
        if book is None:
            return redirect("/?error=Book%20not%20found")

        book_cache.delete(book)
        progress.clear_position(book.title)
        library.remove_book(book.path.name)

        return redirect("/?success=Book%20and%20cache%20deleted")