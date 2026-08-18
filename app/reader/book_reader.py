from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata
from app.library.progress import ProgressManager
from app.library.book_cache import BookCache
from app.core.logger import Logger
from app.core.config import FONT_SIZE_READER


logger = Logger("BookReader")


class BookReader:

    def __init__(self, library=None):

        self.library = library

        self.book = None
        self.chapter = None
        self.page = None
        self.pages = []
        self.page_chapter_indices = []

        self.chapter_index = 0
        self.page_index = 0

        self.paginator = None

        self.progress = ProgressManager()
        
        self.book_cache = BookCache()

    def set_display(self, display):

        font = display.get_font(FONT_SIZE_READER)
        text_bbox = font.getbbox("Ag")
        line_height = (text_bbox[3] - text_bbox[1]) + 5
        footer_y = display.width - 25
        lines_per_page = max(1, (footer_y - 30) // line_height)

        self.paginator = Paginator(
            font=font,
            page_width=display.height,
            lines_per_page=lines_per_page,
            margin=10,
        )

    def open(self, book):

        logger.info("Opening book: %s", book.path)
        logger.debug("Checking book cache")
        cached_book = self.book_cache.load(book)

        if cached_book:
            self.book = cached_book
            logger.info("Loaded book from cache: %s", self.book.title)

        else:
            if self.paginator is None:
                raise RuntimeError("BookReader has no paginator; call set_display() first.")

            logger.debug("Loading EPUB metadata")
            self.book = load_metadata(book.path)
            
            logger.debug("Loading EPUB chapters")
            self.book.chapters = load_chapters(book.path)
            
            logger.info("Paginating %d chapters", len(self.book.chapters))
            for chapter in self.book.chapters:
                self.paginator.paginate_chapter(chapter)

            logger.debug("Saving book cache")
            self.book_cache.save(self.book)

        self.pages = [
            page
            for chapter in self.book.chapters
            for page in chapter.pages
        ]
        self.page_chapter_indices = [
            chapter_index
            for chapter_index, chapter in enumerate(self.book.chapters)
            for _ in chapter.pages
        ]

        position = self.progress.get_position(self.book.title) if cached_book else None
        self.page_index = min(
            position["page"] if position else 0,
            max(0, len(self.pages) - 1),
        )
        self._sync_current_page()

        logger.info(
            "Opened '%s': %d chapters, %d pages",
            self.book.title,
            len(self.book.chapters),
            len(self.pages),
        )

    def _sync_current_page(self):

        self.page = self.current_page()
        self.chapter_index = (
            self.page_chapter_indices[self.page_index]
            if self.page is not None
            else 0
        )

    def current_page(self):

        if not self.pages:
            return None

        return self.pages[self.page_index]


    def next_page(self):

        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self._sync_current_page()
            self.save_position()


    def previous_page(self):

        if self.page_index > 0:
            self.page_index -= 1
            self._sync_current_page()
            self.save_position()


    def save_position(self):

        if self.book is None:
            return

        self.progress.update(
            self.book.title,
            self.chapter_index,
            self.page_index,
        )