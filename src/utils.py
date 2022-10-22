"""Utils"""

from enum import Enum


class Color(Enum):
    BLACK = "1"
    WHITE = "2"

    def __str__(self):
        return self.name
