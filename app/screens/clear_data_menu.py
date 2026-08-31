from pathlib import Path

from app.widgets.menu import MenuItem, MenuScreen
from app.core.logger import Logger

logger = Logger("ClearData")


class ClearDataMenu(MenuScreen):

    def __init__(self, display, assets_dir=None, ui=None, app=None):
        super().__init__(
            display,
            assets_dir,
            ui,
            title="Clear Data",
            items=[
                MenuItem("Clear Progress", action=self.clear_progress),
                MenuItem("Clear Bookmarks", action=self.clear_bookmarks),
                MenuItem("Clear Book Cache", action=self.clear_cache),
                MenuItem("Clear Books", action=self.clear_books),
                MenuItem("Back", action=self.back),
            ],
            app=app,
        )

    def _project_root(self):
        return Path(__file__).resolve().parents[2]

    def clear_progress(self):
        path = self._project_root() / "books" / "data" / "progress.json"
        self._clear_json(path)

    def clear_bookmarks(self):
        path = self._project_root() / "books" / "data" / "bookmarks.json"
        self._clear_json(path)

    def clear_cache(self):
        cache_dir = self._project_root() / "books" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

        for path in cache_dir.glob("*.json"):
            try:
                path.unlink()
                logger.info("Deleted cache file: %s", path)
            except OSError as exc:
                logger.error("Failed to clear cache file %s: %s", path, exc)

    def clear_books(self):
        books_dir = self._project_root() / "books" / "epubs"
        books_dir.mkdir(parents=True, exist_ok=True)

        for path in books_dir.glob("*.epub"):
            try:
                path.unlink()
                logger.info("Deleted book: %s", path)
            except OSError as exc:
                logger.error("Failed to delete book %s: %s", path, exc)

    def _clear_json(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if path.exists():
                path.unlink()
        except OSError as exc:
            logger.error("Failed to clear %s: %s", path, exc)

        try:
            path.write_text("{}\n", encoding="utf-8")
        except OSError as exc:
            logger.error("Failed to reset %s: %s", path, exc)

    def back(self):
        from app.screens.main_menu import MainMenu
        self.ui.show(MainMenu)