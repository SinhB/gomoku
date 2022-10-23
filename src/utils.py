"""Utils"""

from enum import Enum

BLACK_VALUE = "1"
WHITE_VALUE = "2"


class Color(Enum):
    BLACK = BLACK_VALUE
    WHITE = WHITE_VALUE

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    def swap(self):
        if self.value == BLACK_VALUE:
            return Color.WHITE
        return Color.BLACK
