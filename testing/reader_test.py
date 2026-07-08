import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from books.library import Library
from books.parser import Parser


def test_library_and_parser():
    library = Library()

    if not getattr(library, "file_names", None):
        print("No EPUB files found.")
        return

    print("Discovered books:")
    for book_name in library.file_names:
        print(f" - {book_name}")

    for book_name in library.file_names:
        Parser(book_name)


if __name__ == "__main__":
    test_library_and_parser()
