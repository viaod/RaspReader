# Scan books

from pathlib import Path
import glob

class Library:
    
     def __init__(self):
        
        books_path = Path(__file__).parent / "/*.epub"
        
        print(glob.glob(books_path))


if __name__ == "__main__":
    Library()