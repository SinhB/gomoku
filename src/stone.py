"""Class Stone"""

from typing import List

from src.utils import Color


class Stone:
    """
    A gomoku stone piece

    Attributes:
        - color(Color): Color of the stone (black or white)
        - pos_x(int): Position X on the board
        - pos_y(int): Position Y on the board
        - neighbours(List[Stone]): List of the stone's neighbours
    """

    def __init__(self, color, x, y):
        self.color: Color = color
        self.pos_x: int = x
        self.pos_y: int = y
        self.neighbours: List[Stone] = []

    def __repr__(self) -> str:
        return self.color.value

    def coord(self):
        """Return X and Y position of the stone"""
        return self.pos_x, self.pos_y

    def add_neighbour(self, neighbour):
        """Add neighbours to the list"""
        self.neighbours.append(neighbour)

    def remove_neighbour(self, neighbour):
        """Remove a neighbours from the list"""
        self.neighours.remove(neighbour)
