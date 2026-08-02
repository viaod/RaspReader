from app.library.book import Chapter
from app.reader.chapters import load_chapters
from app.reader.paginator import Paginator
from app.library.metadata import load_metadata

class BookReader:
    def __init__(self, library=None):
        self.library = library
        self.parser = Parser()
        self.paginator = Paginator()
        
        # current page functionality ughh...?

    # get book from library and pass to parser then to paginator for display
    def open(self, book):
        # Use the library to get the book content
        book = load_metadata(book.path)
        book.chapters = load_chapters(book.path)
        
        print(book.title)
        print(book.author)

        for chapter in book.chapters:
            print(chapter.title)
        
        # Parse the book content into chapters
        
        # Turn 
        
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