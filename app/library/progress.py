import json
from pathlib import Path
import time


class ProgressManager:

    def __init__(self, path="books/data/progress.json"):
        self.path = Path(path)
        self.path.parent.mkdir(exist_ok=True)
        if not self.path.exists():
            self.save({})

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, progress):
        with open(self.path, "w") as f:
            json.dump(progress, f, indent=4)

    def get_position(self, book_id):
        progress = self.load()
        data = progress.get(str(book_id), {})
        return {
            "chapter": data.get("chapter", 0),
            "page": data.get("page", 0),
        }

    def clear_position(self, book_id):
        progress = self.load()
        key = str(book_id)
        if key in progress:
            del progress[key]
        if progress.get("_last_book") == key:
            progress.pop("_last_book", None)
        self.save(progress)

    def update(self, book_id, chapter, page):
        progress = self.load()
        key = str(book_id)

        progress[key] = {
            "chapter": chapter,
            "page": page,
            "updated_at": time.time(),
        }
        progress["_last_book"] = key
        self.save(progress)

    def get_last_book(self):
        progress = self.load()
        return progress.get("_last_book")

    def get_latest_book(self):
        progress = self.load()

        latest_key = None
        latest_time = -1

        for key, value in progress.items():
            if key.startswith("_"):
                continue

            ts = value.get("updated_at", 0)
            if ts > latest_time:
                latest_time = ts
                latest_key = key

        return latest_key

    def set_last_book(self, book_id):
        progress = self.load()
        progress["_last_book"] = str(book_id)
        self.save(progress)