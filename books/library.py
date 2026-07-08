# Scan books

from pathlib import Path
import glob


class Library:
    def __init__(self):
        # Get the path to the books directory relative to this file
        books_path = Path(__file__).parent / "epubs" / "*.epub"
        
        # Use glob to find all EPUB files in the books directory
        book_files = glob.glob(str(books_path))
        
        # Store the file names in a list
        self.file_names = [Path(path).name for path in book_files]

if __name__ == "__main__":
    Library()