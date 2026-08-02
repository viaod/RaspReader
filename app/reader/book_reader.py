from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata
from app.library.progress import ProgressManager


class BookReader:

    def __init__(self, library=None):

        self.library = library

        self.book = None
        self.chapter = None
        self.page = None
        self.pages = []

        self.chapter_index = 0
        self.page_index = 0

        self.paginator = Paginator(
            chars_per_line=25,
            lines_per_page=14,
        )

        self.progress = ProgressManager()


    def open(self, book):

        # Load the book
        self.book = load_metadata(book.path)
        self.book.chapters = load_chapters(book.path)

        # Load saved position
        position = self.progress.get_position(self.book.title)

        self.chapter_index = position["chapter"]
        self.page_index = position["page"]

        # Clamp chapter index
        if self.chapter_index >= len(self.book.chapters):
            self.chapter_index = 0

        self.chapter = self.book.chapters[self.chapter_index]

        # Paginate current chapter
        self.pages = self.paginator.paginate_chapter(self.chapter)

        # Clamp page index
        if self.page_index >= len(self.pages):
            self.page_index = 0

        self.page = self.pages[self.page_index]


    def current_page(self):

        if not self.pages:
            return None

        return self.pages[self.page_index]


    def next_page(self):

        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self.page = self.pages[self.page_index]
            self.save_position()


    def previous_page(self):

        if self.page_index > 0:
            self.page_index -= 1
            self.page = self.pages[self.page_index]
            self.save_position()


    def save_position(self):

        if self.book is None:
            return

        self.progress.update(
            self.book.title,
            self.chapter_index,
            self.page_index,
        )