from app.library.book import Chapter
from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata

class BookReader:
    def __init__(self, library=None):
        self.library = library
        self.paginator = Paginator(
            chars_per_line=50,
            lines_per_page=18
        )
        
        # current page functionality ughh...?

    # get book from library and pass to parser then to paginator for display
    def open(self, book):
        # Use the library to get the book content
        book = load_metadata(book.path)
        book.chapters = load_chapters(book.path)
        
        # print(book.title)
        # print(book.author)

        # for chapter in book.chapters:
        #     print(chapter.title)
        
        chapter = book.chapters[0]

        pages = paginator.paginate_chapter(chapter)


        print(
            f"{chapter.title}: {len(pages)} pages"
        )


        print(pages[0].text)
        
        
    def close():
        ...
        
    def next_page():
        ...
        
    def previous_page():
        ...
    
    def current_page():
        ...
        
    def chapter_title():
        ...
        
    # TODO: Implement these methods 
    # def go_to_page(page_number):
    #     ...
        
    # def go_to_chapter(chapter_number):
    #     ...