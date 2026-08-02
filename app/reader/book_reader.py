from app.library.book import Chapter
from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata

class BookReader:

    def __init__(self, library=None):

        self.library = library

        self.paginator = Paginator(
            chars_per_line=25,
            lines_per_page=14
        )

        self.pages = []
        self.page_index = 0


    def open(self, book):

        book = load_metadata(book.path)
        book.chapters = load_chapters(book.path)

        chapter = book.chapters[0]

        self.pages = self.paginator.paginate_chapter(
            chapter
        )

        self.page_index = 0



    def current_page(self):

        if not self.pages:
            return None

        return self.pages[self.page_index]



    def next_page(self):

        if self.page_index < len(self.pages)-1:
            self.page_index += 1



    def previous_page(self):

        if self.page_index > 0:
            self.page_index -= 1