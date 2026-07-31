import ebooklib
from ebooklib import epub

from app.library.book import Book


def load_book(path):
    """
    Read an EPUB file and return a Book object.
    """

    epub_book = epub.read_epub(str(path))

    title = path.stem
    author = "Unknown"

    metadata = epub_book.get_metadata("DC", "title")
    if metadata:
        title = metadata[0][0]

    metadata = epub_book.get_metadata("DC", "creator")
    if metadata:
        author = metadata[0][0]

    return Book(
        path=path,
        title=title,
        author=author,
        # description=...,
        # publisher=...,
        # chapters=...,
    )
    
    # def get_title(...)
    # def get_author(...)
    # def get_language(...)
    # def get_cover(...)
    # def get_description(...)
    # def get_publisher(...)
    # def get_date(...)
    # def get_subjects(...)