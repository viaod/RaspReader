from pathlib import Path
import json

from app.library.book import Book, Chapter, Page


class BookCache:


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