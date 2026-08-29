import json
from pathlib import Path


class LibraryState:

    def __init__(self, path="book/data/library.json"):

        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save({
                "offloaded": []
            })

    def load(self):

        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4
            )

    def offload(self, book):

        data = self.load()

        book_id = str(Path(book.path).name)

        if book_id not in data["offloaded"]:
            data["offloaded"].append(book_id)

        self.save(data)

    def restore(self, book):

        data = self.load()

        book_id = str(Path(book.path).name)

        if book_id in data["offloaded"]:
            data["offloaded"].remove(book_id)

        self.save(data)

    def is_offloaded(self, book):

        data = self.load()

        book_id = str(Path(book.path).name)

        return book_id in data["offloaded"]
        
    def get_offloaded(self):
        data = self.load()
        return data.get("offloaded", [])