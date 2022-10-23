"""Class Stone"""

import numpy as np

from src.utils import Color


class Stone:
    """
    A gomoku stone piece

    Attributes:
        - color(Color): Color of the stone (black or white)
        - coordinates(np.array): Coordinates X and Y of the stone in the board
        - neighbours(np.array): List of the stone's neighbours
    """

    def __init__(self, color, coordinates):
        self.color: Color = color
        self.coordinates = np.array(coordinates, ndmin=2, dtype=np.int8)
        self.neighbours: np.array

    def __repr__(self) -> str:
        return self.color.value

    def add_neighbour(self, neighbour):
        """Add neighbours to the list"""
        pass

    def remove_neighbour(self, neighbour):
        """Remove a neighbours from the list"""
        pass
