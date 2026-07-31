from flask import (
    render_template,
    request,
    redirect,
)

from app.web.upload import upload_book


def register_routes(app, library):

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
            return redirect(
                "/?error=Please%20choose%20a%20book"
            )

        try:
            upload_book(file, library)

        except ValueError as e:
            return redirect(
                f"/?error={e}"
            )

        return redirect(
            "/?success=Book%20uploaded%20successfully"
        )