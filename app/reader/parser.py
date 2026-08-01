from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.chapters = []
        
    def parse_book(self, book_content):
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(book_content, 'html.parser')
        
        # Find all chapter elements (assuming they are marked with <h2> tags)
        chapter_elements = soup.find_all('h2')
        
        self.chapters = []
        
        for chapter in chapter_elements:
            chapter_title = chapter.get_text()
            chapter_content = ""
            
            # Get the next siblings until the next <h2> or end of document
            for sibling in chapter.next_siblings:
                if sibling.name == 'h2':
                    break
                if sibling.name is not None:
                    chapter_content += str(sibling)
            
            self.chapters.append({
                'title': chapter_title,
                'content': chapter_content
            })
        
        return self.chapters    