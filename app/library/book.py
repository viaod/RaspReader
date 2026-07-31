from dataclasses import dataclass
from pathlib import Path

@dataclass
class Book:
    path: Path
    title: str
    author: str

    @property
    def filename(self):
        return self.path.name