from pathlib import Path

from app.core.logger import Logger
from app.library.metadata import load_metadata
from app.library.library_state import LibraryState

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

        for path in self.books_dir.glob("*.epub"):
            books.append(load_metadata(path))

        return sorted(books, key=lambda book: book.title.casefold())

    def get_books(self):

        books = []

        for path in self.books_dir.glob("*.epub"):

            book = load_metadata(path)

            if self.state.is_offloaded(book):
                continue

            books.append(book)

        return books

    def add_book(self, uploaded_file):

        destination = self.books_dir / uploaded_file.filename

        uploaded_file.save(destination)

        logger.info(f"Added {uploaded_file.filename}")

        return load_metadata(destination)

    def offload_book(self, book):

        self.state.offload(book)
        
    def restore_book(self, book):
        
        self.state.restore(book)

    def book_exists(self, filename):
        return (self.books_dir / filename).exists()