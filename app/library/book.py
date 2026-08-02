from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Chapter:
    title: str
    text: str


@dataclass
class Book:
    path: Path
    title: str
    author: str

    language: str | None = None
    publisher: str | None = None
    description: str | None = None

    chapters: list[Chapter] = field(default_factory=list)