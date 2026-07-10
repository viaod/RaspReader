from enum import Enum, auto

class Event(Enum):

    ROTATE_LEFT = auto()
    ROTATE_RIGHT = auto()

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    SELECT = auto()

    LONG_PRESS = auto()

    DOUBLE_PRESS = auto()

    NONE = auto()