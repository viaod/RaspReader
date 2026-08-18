from pathlib import Path
import json

from app.library.book import Book, Chapter, Page
from app.core.config import TEXT_SCALE


class BookCache:

    CACHE_VERSION = 2


    def __init__(self, cache_dir=None):

        self.cache_dir = Path(
            cache_dir
            or Path(__file__).resolve().parent.parent.parent / "books/cache"
        )

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def cache_path(self, book):

        return self.cache_dir / f"{Path(book.path).stem}.json"

    def exists(self, book):

        return self.cache_path(book).exists()

    def delete(self, book):

        path = self.cache_path(book)

        if not path.exists():
            return False

        path.unlink()
        return True

    def load(self, book):

        path = self.cache_path(book)

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Older caches used the tiny fixed Pillow font and therefore have
        # incompatible line breaks with the scalable typography.
        if (data.get("version") != self.CACHE_VERSION or
                data.get("text_scale") != TEXT_SCALE):

            return None

        cached_book = Book(
            title=data["title"],
            author=data["author"],
            path=book.path,
        )

        cached_book.chapters = []

        for chapter_data in data["chapters"]:

            chapter = Chapter(
                title=chapter_data["title"],
                text="",
            )

            chapter.pages = []

            for page_data in chapter_data["pages"]:

                chapter.pages.append(
                    Page(
                        number=page_data["number"],
                        text=page_data["text"],
                    )
                )

            cached_book.chapters.append(chapter)

        return cached_book

    def save(self, book):

        data = {
            "version": self.CACHE_VERSION,
            "text_scale": TEXT_SCALE,
            "title": book.title,
            "author": book.author,
            "chapters": [],
        }

        for chapter in book.chapters:

            data["chapters"].append(
                {
                    "title": chapter.title,
                    "pages": [
                        {
                            "number": page.number,
                            "text": page.text,
                        }
                        for page in chapter.pages
                    ],
                }
            )

        with open(self.cache_path(book), "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4,
            )