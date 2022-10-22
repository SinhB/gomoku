"""Class Board"""

from typing import Dict, List

from termcolor import colored

from src.stone import Stone

BLACK_STONE_COLOR = "red"
WHITE_STONE_COLOR = "blue"

COLOR_REPLACEMENT = {
    "1": colored("1", BLACK_STONE_COLOR),
    "2": colored("2", WHITE_STONE_COLOR),
}


class Board:
    """
    A Gomoku Ninuki board
    Attributes:
        - size(int): Size of an board edge. Default to 19
        - _board(List[List[any]): 2D board,
            containing 0(int) for blank and Stone objects
    """

    def __init__(self, size=19) -> None:
        self._size: int = size
        self._board: List[List[any]] = self.create(size)

    def create(self, size: int):
        """Create a 2D board of size: size"""
        return [[0 for _ in range(size)] for _ in range(size)]

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

    def update(self, stone: Stone):
        """Update the board by adding a stone"""
        self._board[stone.pos_y][stone.pos_x] = stone
        return self._board
