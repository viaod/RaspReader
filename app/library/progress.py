import json
from pathlib import Path


class ProgressManager:

    def __init__(self, path="data/progress.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            exist_ok=True
        )

        if not self.path.exists():
            self.save({})


    def load(self):

        with open(self.path, "r") as f:
            return json.load(f)


    def save(self, progress):

        with open(self.path, "w") as f:
            json.dump(
                progress,
                f,
                indent=4
            )


    def get_position(self, book_id):

        progress = self.load()

        return progress.get(
            book_id,
            {
                "chapter": 0,
                "page": 0
            }
        )


    def update(
        self,
        book_id,
        chapter,
        page
    ):

        progress = self.load()

        progress[book_id] = {
            "chapter": chapter,
            "page": page
        }

        self.save(progress)