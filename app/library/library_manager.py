from pathlib import Path

from app.core.logger import Logger
from app.library.metadata import load_metadata

logger = Logger("Library")


class LibraryManager:

    def __init__(self, books_dir=None):

        self.books_dir = Path(
            books_dir
            or Path(__file__).resolve().parent.parent.parent / "books/epubs"
        )

        self.books_dir.mkdir(exist_ok=True)

    def get_books(self):

        books = []

        for path in sorted(self.books_dir.glob("*.epub")):
            books.append(load_metadata(path))

        return books

    def get_book(self, filename):

        path = self.books_dir / filename

        if not path.exists():
            return None

        return load_metadata(path)

    def add_book(self, uploaded_file):

        destination = self.books_dir / uploaded_file.filename

        uploaded_file.save(destination)

        logger.info(f"Added {uploaded_file.filename}")

        return load_metadata(destination)

    def remove_book(self, filename):

        path = self.books_dir / filename

        if path.exists():
            path.unlink()
            logger.info(f"Removed {filename}")
            return True

        return False

    def book_exists(self, filename):
        return (self.books_dir / filename).exists()