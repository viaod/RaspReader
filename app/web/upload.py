from pathlib import Path


ALLOWED_EXTENSIONS = {".epub"}


def upload_book(file, library):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only EPUB files are supported.")

    if library.book_exists(file.filename):
        raise ValueError("That book already exists.")

    library.add_book(file)
    