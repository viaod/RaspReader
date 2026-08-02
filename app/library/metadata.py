from pathlib import Path

from ebooklib import epub

from .book import Book


def _get_metadata(book, key, default=None):

    value = book.get_metadata("DC", key)

    if value:
        return value[0][0]

    return default


def load_metadata(path: Path):

    epub_book = epub.read_epub(str(path))

    return Book(
        path=path,
        title=_get_metadata(epub_book, "title", path.stem),
        author=_get_metadata(epub_book, "creator", "Unknown"),
        language=_get_metadata(epub_book, "language"),
        publisher=_get_metadata(epub_book, "publisher"),
        description=_get_metadata(epub_book, "description"),
    )