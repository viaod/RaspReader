from app.library.book import Chapter
from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata
from app.library.progress import ProgressManager

class BookReader:

    def __init__(self, library=None):

        self.library = library
        
        self.paginator = Paginator(
            chars_per_line=25,
            lines_per_page=14
        )

        self.progress = ProgressManager()

        self.pages = []
        self.page_index = 0
        self.chapter_index = 0


    def open(self, book):

        book = load_metadata(book.path)
        book.chapters = load_chapters(book.path)

        self.book = book

        position = self.progress.get_position(
            book.title
        )

        self.chapter_index = position["chapter"]


        chapter = book.chapters[
            self.chapter_index
        ]


        self.pages = self.paginator.paginate_chapter(
            chapter
        )


        self.page_index = position["page"]



    def current_page(self):

        if not self.pages:
            return None

        return self.pages[self.page_index]



    def next_page(self):

        if self.page_index < len(self.pages)-1:

            self.page_index += 1

            self.save_position()


    def previous_page(self):

        if self.page_index > 0:

            self.page_index -= 1

            self.save_position()
            
    def save_position(self):

        self.progress.update(
            self.book.title,
            self.chapter_index,
            self.page_index
        )