"""Class Board"""

from typing import Dict

import numpy as np
from termcolor import colored

from src.stone import Stone
from src.utils import (BLACK_SEQUENCES, BLACK_VALUE, WHITE_VALUE, Color,
                       change_sequences_to_white, timeit)

BLACK_STONE_COLOR = "red"
WHITE_STONE_COLOR = "blue"

COLOR_REPLACEMENT = {
    BLACK_VALUE: colored(BLACK_VALUE, BLACK_STONE_COLOR),
    WHITE_VALUE: colored(WHITE_VALUE, WHITE_STONE_COLOR),
}


class Board:
    """
    A Gomoku Ninuki board

    Attributes
    ----------
    size(int)          : Size of an board edge. Default to 19
    _board(np.ndarray) : 2D board, containing 0(int8)
    for blank and Stone objects
    coordinates(dict)  : Containing all coordinates
    from black and white stones
    """

    def __init__(self, color, size=19) -> None:
        self.color: Color = color
        self._size: int = size
        self._board: np.ndarray = self.create(size)
        self.coordinates = {Color.WHITE: None, Color.BLACK: None}
        self.score: int = 0
        self.sequence_frequence = {
            "five": 0,
            "open_four": 0,
            "simple_four": 0,
            "open_three": 0,
            "broken_three": 0,
            "simple_three": 0,
        }

    def create(self, size: int):
        """Create a 2D board

        Parameters
        ----------
        size   : size for width and height

        Output
        ------
        Output : 2D Array representing the board.
        """
        return np.zeros((size, size), dtype=np.int8)

    def add_stone_coordinates(self, stone: Stone):
        """Get all stones coordinates

        Parameters
        ----------
        stone  : Stone object
        """
        if self.coordinates[stone.color] is None:
            self.coordinates[stone.color] = stone.coordinates
        else:
            self.coordinates[stone.color] = np.append(
                self.coordinates[stone.color], stone.coordinates, axis=0
            )

    def get_stones_coordinates(self):
        """Get all stones coordinates

        Output
        ------
        Output : 2D Array for each color,
        representing the coordinates for each stones.
        """
        black_coordinates = np.argwhere(self._board == BLACK_VALUE)
        white_coordinates = np.argwhere(self._board == WHITE_VALUE)
        return black_coordinates, white_coordinates

    def update(self):
        """Update the board by adding stones

        Output
        ------
        Output : 2D Array representing the board.
        """
        coord = self.coordinates
        self._board[
            coord[Color.WHITE][:, 0], coord[Color.WHITE][:, 1]
        ] = Color.WHITE.value
        self._board[
            coord[Color.BLACK][:, 0], coord[Color.BLACK][:, 1]
        ] = Color.BLACK.value
        return self._board

    def get_available_pos(self):
        """ """
        all_stones = np.concatenate(
            (self.coordinates[Color.WHITE], self.coordinates[Color.BLACK]), axis=0
        )
        moves = np.array(
            [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
        )
        possible_pos = np.vstack(all_stones + moves[:, None])
        possible_pos = possible_pos[
            np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
        ]
        print(f"Possible moves: {len(possible_pos)}")
        return possible_pos

    def place_available_pos(self):
        """ """
        pos = self.get_available_pos()
        b = self._board
        np.put(b, np.ravel_multi_index(pos.T, b.shape), 3)

    def get_diagonals(self):
        """Get diagonals of the current board

        Output
        ------
        Output : 2D Array representing a diagonal on each row.
        """
        b = self._board
        # lower-left-to-upper-right
        diags = [b[::-1, :].diagonal(i) for i in range(-b.shape[0] + 1, b.shape[1])]
        # upper-left-to-lower-right
        diags.extend(b.diagonal(i) for i in range(b.shape[1] - 1, -b.shape[0], -1))
        # remove only zeros diagonals
        diags = [d for d in diags if ~np.all(d == 0)]
        # Make an 2d array from padding diagonals with "3"
        # (can't interfer with sequence search)
        max_d_length = max(len(d) for d in diags)
        diags = np.array(
            [np.pad(d, (0, max_d_length - len(d)), constant_values=3) for d in diags]
        )
        return diags

    def get_rows(self):
        """Get rows of the current board

        Output
        ------
        Output : 2D Array representing a row on each row.
        """
        b = self._board
        # remove only zeros rows
        rows = b[~np.all(b == 0, axis=1)]
        return rows

    def get_columns(self):
        """Get columns of the current board

        Notes
        -----
        Seems like it's faster to transpose the board then
        do some calcul row wise than calculate using axis 0

        Output
        ------
        Output : 2D Array representing a columns on each row.
        """
        b = self._board
        columns = b.T
        # remove only zeros columns
        columns = columns[~np.all(columns == 0, axis=1)]
        return columns

    def search_sequence(self, arr, seq, seq_type, seq_list):
        """Find sequence in an array using NumPy only.

        Parameters
        ----------
        arr      : input 1D array
        seq      : input 1D array
        seq_type : name of the sequence
        seq_list : score associate to the sequence type
        """

        # Store sizes of input array and sequence
        Na, Nseq = arr.size, seq.size

        # Range of sequence
        r_seq = np.arange(Nseq)

        # Create a 2D array of sliding indices across the entire length of
        # input array.
        # Match up with the input sequence & get the matching starting indices.
        M = (arr[np.arange(Na - Nseq + 1)[:, None] + r_seq] == seq).all(1)

        # Get the range of those indices as final output
        if M.any() > 0:
            self.sequence_frequence[seq_type] += M.sum()
            s_tmp = M.sum() * (seq_list[1] * seq_list[2])
            self.score += s_tmp

    @timeit
    def get_score(self):
        """Get the score of the current board

        The score is calculated comparing each rows, columns, diagonals
        with sequences, and if a sequence is found, attribute a score
        depending on the sequence type
        """
        if self.color == Color.BLACK:
            seq = BLACK_SEQUENCES
        else:
            seq = change_sequences_to_white()

        diags = self.get_diagonals()
        rows = self.get_rows()
        columns = self.get_columns()

        for seq_type, seq_list in seq.items():
            for s in seq_list[0]:
                np.apply_along_axis(
                    self.search_sequence, 1, diags, s, seq_type, seq_list
                )
                np.apply_along_axis(
                    self.search_sequence, 1, rows, s, seq_type, seq_list
                )
                np.apply_along_axis(
                    self.search_sequence, 1, columns, s, seq_type, seq_list
                )
        print(f"Score dict : {self.sequence_frequence}")
        print(f"Score total: {self.score}")

    def display(self):
        """Print the board

        Print the board in the terminal with colors for each stone type
        """

        def _color_black_and_white(row: str, replacement: Dict):
            for item, rep in replacement.items():
                row = row.replace(str(item), rep)
            return row

        for row in self._board:
            str_row = "".join(str(row)).translate({ord(char): "" for char in "[,]"})
            colored_row = _color_black_and_white(str_row, COLOR_REPLACEMENT)
            print(colored_row)
