"""Class Board"""

from typing import Dict

import numpy as np
from termcolor import colored

from src.stone import Stone
from src.utils import BLACK_VALUE, WHITE_VALUE, Color

BLACK_STONE_COLOR = "red"
WHITE_STONE_COLOR = "blue"

COLOR_REPLACEMENT = {
    BLACK_VALUE: colored(BLACK_VALUE, BLACK_STONE_COLOR),
    WHITE_VALUE: colored(WHITE_VALUE, WHITE_STONE_COLOR),
}


class Board:
    """
    A Gomoku Ninuki board
    Attributes:
        - size(int): Size of an board edge. Default to 19
        - _board(np.ndarray): 2D board,
            containing 0(int8) for blank and Stone objects
        - coordinates(dict): Containing all coordinates from black and white stones
    """

    def __init__(self, size=19) -> None:
        self._size: int = size
        self._board = self.create(size)
        self.coordinates = {Color.WHITE: None, Color.BLACK: None}

    def create(self, size: int):
        """Create a 2D board of size: size filled by zeros"""
        return np.zeros((size, size), dtype=np.int8)

    def add_stone_coordinates(self, stone: Stone):
        if self.coordinates[stone.color] is None:
            self.coordinates[stone.color] = stone.coordinates
        else:
            self.coordinates[stone.color] = np.append(
                self.coordinates[stone.color], stone.coordinates, axis=0
            )
        print(self.coordinates)

    def update(self):
        """Update the board by adding stones"""
        coord = self.coordinates
        self._board[
            np.ix_(coord[Color.WHITE][:, 0], coord[Color.WHITE][:, 1])
        ] = Color.WHITE.value
        self._board[
            np.ix_(coord[Color.BLACK][:, 0], coord[Color.BLACK][:, 1])
        ] = Color.BLACK.value
        return self._board

    def display(self):
        """Print the board"""

        def _color_black_and_white(row: str, replacement: Dict):
            for item, rep in replacement.items():
                row = row.replace(item, rep)
            return row

        for row in self._board:
            str_row = "".join(str(row)).translate({ord(char): "" for char in "[,]"})
            colored_row = _color_black_and_white(str_row, COLOR_REPLACEMENT)
            print(colored_row)
