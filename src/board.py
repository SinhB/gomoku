"""Class Board"""

from typing import Dict

import numpy as np
from termcolor import colored

from src.utils import BLACK_VALUE, SEQUENCES, WHITE_VALUE, Color, timeit

BLACK_STONE_COLOR = "red"
WHITE_STONE_COLOR = "blue"

COLOR_REPLACEMENT = {
    WHITE_VALUE: colored(2, WHITE_STONE_COLOR),
    BLACK_VALUE: colored(BLACK_VALUE, BLACK_STONE_COLOR),
}


class BoardState:
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

    def __init__(
        self, color, size=19, board=None, coordinates=None, seq_frequence=None
    ) -> None:
        self.color: Color = color
        self._size: int = size
        self._board: np.ndarray = board if board is not None else self.create(size)
        self.coordinates = coordinates or {Color.WHITE: None, Color.BLACK: None}
        self.score: int = 0
        self.sequence_frequence = seq_frequence or {
            Color.BLACK: {
                "five": 0,
                "open_four": 0,
                "simple_four": 0,
                "open_three": 0,
                "broken_three": 0,
                "simple_three": 0,
            },
            Color.WHITE: {
                "five": 0,
                "open_four": 0,
                "simple_four": 0,
                "open_three": 0,
                "broken_three": 0,
                "simple_three": 0,
            },
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

    def add_stone_coordinates(self, color, position):
        """Get all stones coordinates

        Parameters
        ----------
        stone  : Stone object
        """
        position = np.array(position, ndmin=2, dtype=np.int8)
        if self.coordinates[color] is None:
            self.coordinates[color] = position
        else:
            self.coordinates[color] = np.append(
                self.coordinates[color], position, axis=0
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

    def copy(self):
        """ """
        b = np.copy(self._board)
        return BoardState(
            color=self.color.swap(),
            size=self._size,
            board=b,
            coordinates=self.coordinates,
            seq_frequence=self.sequence_frequence,
        )

    def next(self, position):
        """ """
        color = self.color.swap()
        next_state = self.copy()
        if self.is_legal_move(color, position):
            next_state.add_stone_coordinates(color, position)
            next_state.update()
            return next_state
        return None

    def is_legal_move(self, color, position):
        """ """
        if self._board[position[0], position[1]] != 0:
            return False
        b = self.copy()
        actual_open_three = self.sequence_frequence["open_three"]
        b.add_stone_coordinates(color, position)
        b.update()
        b.get_score()
        if b.sequence_frequence["open_three"] >= actual_open_three + 2:
            return False
        return True

    def get_available_pos(self):
        """ """
        all_stones = np.concatenate(
            (self.coordinates[Color.WHITE], self.coordinates[Color.BLACK]), axis=0
        )
        moves = np.array(
            [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
        )
        possible_pos = np.vstack(all_stones + moves[:, None])
        in_board = (
            (possible_pos[:, 0] >= 0)
            & (possible_pos[:, 0] < self._board.shape[0])
            & (possible_pos[:, 1] >= 0)
            & (possible_pos[:, 1] < self._board.shape[1])
        )
        possible_pos = possible_pos[in_board, :]
        possible_pos = possible_pos[
            np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
        ]
        print(f"Possible moves: {len(possible_pos)}")
        return possible_pos

    def place_available_pos(self):
        """For debug purpose"""
        pos = self.get_available_pos()
        # b = np.copy(self._board)
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

    def search_sequence(self, arr, seq, seq_type):
        """Find sequence in an array using NumPy only.

        Parameters
        ----------
        arr      : input 1D array
        seq      : input 1D array
        seq_type : name of the sequence
        seq_list : score associate to the sequence type
        """

        black_seq = seq * Color.BLACK.value
        white_seq = seq * Color.WHITE.value

        # Store sizes of input array and sequence
        Na, Nseq = arr.size, seq.size

        # Range of sequence
        r_seq = np.arange(Nseq)

        # Create a 2D array of sliding indices across the entire length of
        # input array.
        # Match up with the input sequence & get the matching starting indices.
        black_match = (arr[np.arange(Na - Nseq + 1)[:, None] + r_seq] == black_seq).all(
            1
        )
        white_match = (arr[np.arange(Na - Nseq + 1)[:, None] + r_seq] == white_seq).all(
            1
        )

        # Get the range of those indices as final output
        if black_match.any() > 0:
            self.sequence_frequence[Color.BLACK][seq_type] += black_match.sum()
        if white_match.any() > 0:
            self.sequence_frequence[Color.WHITE][seq_type] += white_match.sum()

    @timeit
    def get_sequence_frequences(self):
        """Get the score of the current board

        The score is calculated comparing each rows, columns, diagonals
        with sequences, and if a sequence is found, attribute a score
        depending on the sequence type
        """

        diags = self.get_diagonals()
        rows = self.get_rows()
        columns = self.get_columns()

        for seq_type, seq_list in SEQUENCES.items():
            for s in seq_list[0]:
                np.apply_along_axis(self.search_sequence, 1, diags, s, seq_type)
                np.apply_along_axis(self.search_sequence, 1, rows, s, seq_type)
                np.apply_along_axis(self.search_sequence, 1, columns, s, seq_type)
        print(f"Score dict : {self.sequence_frequence}")

    @timeit
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
            str_row = " ".join(str_row.split())
            colored_row = _color_black_and_white(str_row, COLOR_REPLACEMENT)
            print(colored_row)
