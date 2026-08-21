import json
from pathlib import Path


class BookmarkManager:

    def __init__(self, path="books/data/bookmarks.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save({})

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, bookmarks):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(bookmarks, file, ensure_ascii=False, indent=4)

    def add(self, book_id, chapter, page):
        """Save a page bookmark, returning False when it already exists."""
        bookmarks = self.load()
        book_bookmarks = bookmarks.setdefault(book_id, [])
        bookmark = {"chapter": chapter, "page": page}

        if bookmark in book_bookmarks:
            return False

        book_bookmarks.append(bookmark)
        self.save(bookmarks)
        return True

    def get_bookmarks(self, book_id):
        """Return bookmarks for a book in the order they were saved."""
        return self.load().get(book_id, [])

    def remove(self, book_id, chapter, page):
        """Remove a bookmark, returning False when it does not exist."""
        bookmarks = self.load()
        bookmark = {"chapter": chapter, "page": page}
        book_bookmarks = bookmarks.get(book_id, [])

        if bookmark not in book_bookmarks:
            return False

        book_bookmarks.remove(bookmark)
        if not book_bookmarks:
            del bookmarks[book_id]

        self.save(bookmarks)
        return True
