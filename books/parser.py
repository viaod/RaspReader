# EPUB/TXT support

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


class Parser:

    def __init__(self):

        # Load the EPUB book
        book = epub.read_epub("prideandprejudice.epub")

        print(book.get_metadata("DC", "title"))
        print(book.get_metadata("DC", "creator"))
        
        # # Extract all HTML documents (chapters) from the book
        # chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        # for chapter in chapters:
        #     # Get raw HTML content
        #     content = chapter.get_content()

        #     # Use BeautifulSoup to strip HTML tags and extract readable text
        #     soup = BeautifulSoup(content, 'html.parser')
        #     text = soup.get_text()

        #     # Print page/chapter text (or send to an e-paper display)
        #     print(text)


if __name__ == "__main__":
    Parser()
        
