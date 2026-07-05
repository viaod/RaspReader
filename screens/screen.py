from pathlib import Path


class Screen:

    def __init__(self, display):
        self.display = display

    @property
    def assets(self):
        return (
            Path(__file__).parent.parent
            / "assets"
        )

    def show(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement show()"
        )