"""Class Board"""

from copy import deepcopy
from typing import Dict

import numpy as np
from termcolor import colored

from src.algorithm import evaluate_state, minimax
from src.heuristic import get_numba_sequence_frequences
from src.utils import BLACK_VALUE, WHITE_VALUE, Color, timeit

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
        self, color, size=19, board=None, coordinates=None, sequence_frequences=None
    ) -> None:
        self.color: Color = color
        self._size: int = size
        self._board: np.ndarray = (
            board if board is not None else self.create_int_board(size)
        )
        self.coordinates = coordinates or {Color.WHITE: None, Color.BLACK: None}
        self.sequence_frequences = sequence_frequences or {
            Color.BLACK: {
                "five": 0,
                "open_four": 0,
                "simple_four": 0,
                "open_three": 0,
                "broken_three": 0,
                "simple_three": 0,
                "open_two": 0,
                "broken_two": 0,
                "simple_two": 0,
            },
            Color.WHITE: {
                "five": 0,
                "open_four": 0,
                "simple_four": 0,
                "open_three": 0,
                "broken_three": 0,
                "simple_three": 0,
                "open_two": 0,
                "broken_two": 0,
                "simple_two": 0,
            },
        }

    def create_int_board(self, size: int):
        """Create a 2D board

        Parameters
        ----------
        size   : size for width and height

        Output
        ------
        Output : 2D Array representing the board.
        """
        return np.zeros((size, size), dtype=np.int8)

    def add_stone_coordinates(self, position):
        """Get all stones coordinates

        Parameters
        ----------
        stone  : Stone object
        """
        color = self.color.swap()
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

    def update_board(self):
        """Update the board by adding stones

        Output
        ------
        Output : 2D Array representing the board.
        """
        coord = self.coordinates
        if coord[Color.WHITE] is not None:
            self._board[
                coord[Color.WHITE][:, 0], coord[Color.WHITE][:, 1]
            ] = Color.WHITE.value
        if coord[Color.BLACK] is not None:
            self._board[
                coord[Color.BLACK][:, 0], coord[Color.BLACK][:, 1]
            ] = Color.BLACK.value
        return self._board

    def copy_to_next(self):
        """Copy the current state while swaping its color

        Output
        ------
        Output : New BoardState object
        """
        board_copy = deepcopy(self)
        board_copy.color = self.color.swap()
        return board_copy

    def copy(self):
        """Copy the current state

        Output
        ------
        Output : New BoardState object
        """
        return deepcopy(self)

    # @timeit
    def next(self, position):
        """Copy the current state while swaping its color

        Parameters
        ----------
        position  : [x, y] add the position to the new state
        Output
        ------
        Output    : New BoardState object
        """

        next_state = self.copy_to_next()
        # next_state = BoardState(
        #     color=self.color.swap(),
        #     size=self._size,
        #     board=self._board,
        #     coordinates=self.coordinates,
        #     sequence_frequences=self.sequence_frequences)
        next_state.add_stone_coordinates(position)
        next_state.update_board()
        return next_state

    def is_finished(self):
        # Check capture winning
        # Check Five in a row & not breakable & opponent doesn't win by capture
        pass

    @timeit
    def get_best_move(self, depth, is_maximiser):
        sorted_moves = self.get_best_moves(is_maximiser)
        best_score = -9999 if is_maximiser else 9999
        for scored_move in sorted_moves:
            move_pos = scored_move[1]
            score = minimax(
                self.next(move_pos),
                np.iinfo(np.int32).min,
                np.iinfo(np.int32).max,
                depth - 1,
                not is_maximiser,
            )
            if (is_maximiser and score > best_score) or (
                not is_maximiser and score < best_score
            ):
                best_score = score
                best_move = move_pos
        return best_move, best_score

    # @timeit
    def get_best_moves(self, is_maximiser):
        """ """
        available_positions = self.get_available_pos()
        # legal_positions = self.remove_illegal_pos(available_positions)
        best_moves = self.sort_moves(available_positions, 10, is_maximiser)
        return best_moves

    def remove_illegal_pos(self, positions):
        # for position in positions:
        # if not self.is_legal_move(position):
        #     # delete position
        #     pass
        return positions

    def sort_moves(self, positions, n, is_maximiser):
        moves = []
        for position in positions:
            evaluation = evaluate_state(self.next(position), self.color)
            # print(f"evaluation = {evaluation} for pos: {position} as {self.color}")
            moves.append((evaluation, position))
        # print("-----------------------MOVES--------------------")
        # print(moves)
        return sorted(moves, key=lambda x: x[0], reverse=is_maximiser)[:n]

    # @timeit
    def is_legal_move(self, position):
        """Check if the given position is possible

        Output
        ------
        Output : Boolean
        """
        if self._board[position[0], position[1]] != 0:
            return False
        if not (
            (position[0] >= 0 & position[0] < self._size)
            & (position[1] >= 0 & position[1] < self._size)
        ):
            return False

        # actual_open_three = self.sequence_frequences[self.color]["open_three"]

        b = self.copy()
        b.add_stone_coordinates(position)
        b.update_board()

        # d = get_numba_sequence_frequences(b._board)
        # print(f"Sequence number: {d}")
        score = evaluate_state(b, self.color)
        print(score)

        # Call condition to check if new pos is legal
        # if b.sequence_frequences[self.color]["open_three"] >= actual_open_three + 2:
        #     return False
        return True

    # @timeit
    def get_available_pos(self):
        """Calculate the possible positions

        Positions are 1 radius around all current known positions

        Output
        ------
        Output : 2D array of all possible positions"""
        if (
            self.coordinates[Color.WHITE] is not None
            and self.coordinates[Color.BLACK] is not None
        ):
            all_stones = np.concatenate(
                (self.coordinates[Color.WHITE], self.coordinates[Color.BLACK]), axis=0
            )
        else:
            all_stones = self.coordinates[Color.WHITE] or self.coordinates[Color.BLACK]
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
        possible_pos = np.unique(
            possible_pos[
                np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
            ],
            axis=0,
        )
        return possible_pos

    # def place_available_pos(self, pos=None):
    #     """For debug purpose"""
    #     if pos is None:
    #         pos = self.get_available_pos()
    #     # b = np.copy(self._board)
    #     b = self._board
    #     np.put(b, np.ravel_multi_index(pos.T, b.shape), 3)

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
