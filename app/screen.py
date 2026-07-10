from pathlib import Path


class Screen:
    def __init__(self, display, assets_dir=None):
        self.display = display
        self.assets_dir = Path(assets_dir or Path(__file__).resolve().parent.parent / "assets")

    def show(self):
        raise NotImplementedError("Screen subclasses must implement show()")
