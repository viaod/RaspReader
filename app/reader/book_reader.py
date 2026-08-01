from app.reader.parser import Parser
from app.reader.paginator import Paginator
from app.library.metadata import load_text


class BookReader:
    def __init__(self, library=None):
        self.library = library
        self.parser = Parser()
        self.paginator = Paginator()
        
        # current page functionality ughh...?

    # get book from library and pass to parser then to paginator for display
    def open(self, book):
        # Use the library to get the book content
        book_content = load_text(book.path)
        
        print(type(book_content))
        print(len(book_content))
        print(book_content[:200])
        
        # parsed_book = self.parser.parse_book(book_content)
        # print(parsed_book[:100])  
        # Print the first 100 characters of the parsed book for debugging
        
        
        # # Parse the book content into chapters
        # self.parser.chapters = self.parse_book(book_content)
        
        # # Paginate the parsed chapters into pages
        # self.paginator.pages = self.paginate_chapters(self.parser.chapters)
        
        # # Reset current page index
        # self.paginator.current_page_index = 0
        
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