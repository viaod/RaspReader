from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Page:
    number: int
    text: str


@dataclass
class Chapter:
    title: str
    text: str
    pages: list[Page] = field(default_factory=list)


@dataclass
class Book:
    path: Path
    title: str
    author: str

    language: str | None = None
    publisher: str | None = None
    description: str | None = None

    chapters: list[Chapter] = field(default_factory=list)