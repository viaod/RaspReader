from pathlib import Path
import json


class BookCache:

    def __init__(self, cache_dir=None):
        
        self.cache_dir = Path(
            cache_dir
            or Path(__file__).resolve().parent.parent.parent / "books/cache"
        )

        self.cache_dir.mkdir(parents=True, exist_ok=True)


    def cache_path(self, book):

        return self.cache_dir / f"{Path(book.path).stem}.json"


    def exists(self, book):

        return self.cache_path(book).exists()


    def load(self, book):

        with open(self.cache_path(book), "r", encoding="utf-8") as f:
            return json.load(f)


    def save(self, book_data, book):

        with open(self.cache_path(book), "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False)