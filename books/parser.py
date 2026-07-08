# EPUB/TXT support
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, book_name=None):
        
        books_dir = Path(__file__).parent
        book_path = books_dir / "epubs" / book_name

        book = epub.read_epub(book_path)

        self.metadata = {
            "title": book.get_metadata("DC", "title")[0][0] if book.get_metadata("DC", "title") else None,
            "creator": book.get_metadata("DC", "creator")[0][0] if book.get_metadata("DC", "creator") else None,
        }

        self.chapters = []
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        for chapter in chapters:
            content = chapter.get_content()
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text()
            self.chapters.append(text)

        # print(f"Parsing: {book_path.name}")
        # print(f"Title: {self.metadata['title']}")
        # print(f"Creator: {self.metadata['creator']}")
        # print(f"Loaded {len(self.chapters)} chapter(s)")


if __name__ == "__main__":
    Parser()

