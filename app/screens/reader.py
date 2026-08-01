from app.screen import Screen
from app.core.events import Event

class ReaderScreen(Screen):
    
    def show(self):
        ...
        #time on top right
        #TODO: add battery icon on top left
        
        # page number on bottom left
        # percentage on bottom right 
        
    def handle_input(self, event):
        
        # Select ReaderMenu 
        if event == Event.SELECT:
            from app.screens.reader_menu import ReaderMenuScreen
            self.ui.show(ReaderMenuScreen)
            
        # Left previous page
        if event == Event.RIGHT:
            ...
            
        # Right next page
        if event == Event.LEFT:
            ...
