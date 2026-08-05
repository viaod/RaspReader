from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata
from app.library.progress import ProgressManager
from app.library.book_cache import BookCache


class BookReader:

    def __init__(self, library=None):

        self.library = library

        self.book = None
        self.chapter = None
        self.page = None
        self.pages = []

        self.chapter_index = 0
        self.page_index = 0

        self.paginator = None

        self.progress = ProgressManager()
        
        self.book_cache = BookCache()

    def set_display(self, display):

        font = display.get_font(24)

        self.paginator = Paginator(
            font=font,
            page_width=display.height,
            lines_per_page=9,
            margin=10,
        )

    def open(self, book):

        print(f"BookReader.open: id={id(self)}, book={book.path}", flush=True)
        print("BookReader: checking cache", flush=True)
        cached_book = self.book_cache.load(book)

        if cached_book:
            self.book = cached_book
            print("BookReader: loaded from cache", flush=True)

        else:
            if self.paginator is None:
                raise RuntimeError("BookReader has no paginator; call set_display() first.")

            print("BookReader: loading metadata", flush=True)
            self.book = load_metadata(book.path)
            print("BookReader: loading chapters", flush=True)
            self.book.chapters = load_chapters(book.path)
            print(
                f"BookReader: paginating {len(self.book.chapters)} chapters",
                flush=True,
            )

            for chapter in self.book.chapters:
                self.paginator.paginate_chapter(chapter)

            print("BookReader: saving cache", flush=True)
            self.book_cache.save(self.book)

        self.pages = [
            page
            for chapter in self.book.chapters
            for page in chapter.pages
        ]
        self.page_index = 0
        self.page = self.current_page()
            
        print("BookReader id:", id(self))
            
        print("Book:", self.book.title)
        print("Chapters:", len(self.book.chapters))
        print("Current chapter:", self.chapter_index)
        print("Pages:", len(self.pages))
        print("Current page index:", self.page_index)

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