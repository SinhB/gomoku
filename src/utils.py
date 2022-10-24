"""Utils"""

import time
from enum import Enum
from functools import wraps

import numpy as np

BLACK_VALUE = 1
WHITE_VALUE = 2

BLACK_SEQUENCES = {
    "five": [[np.array((1, 1, 1, 1, 1))], 5, 1],
    "open_four": [
        [
            np.array((0, 1, 1, 1, 1, 0)),
            np.array((2, 1, 1, 0, 1, 1, 0, 1, 1, 2)),
            np.array((2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2)),
        ],
        4,
        2,
    ],
    "simple_four": [
        [
            np.array((2, 1, 1, 1, 1, 0)),
            np.array((0, 1, 1, 1, 1, 2)),
            np.array((0, 1, 1, 0, 1, 1, 0)),
        ],
        4,
        1,
    ],
    "open_three": [
        [
            np.array((0, 0, 1, 1, 1, 0, 0)),
            np.array((0, 1, 0, 1, 1, 0, 1, 0)),
            np.array((1, 0, 1, 0, 1, 0, 1, 0, 1)),
        ],
        3,
        3,
    ],
    "broken_three": [
        [
            np.array((0, 1, 0, 1, 1, 0)),
            np.array((2, 0, 1, 1, 1, 0, 0)),
            np.array((0, 0, 1, 1, 1, 0, 2)),
        ],
        3,
        2,
    ],
    "simple_three": [
        [
            np.array((2, 1, 1, 1, 0)),
            np.array((0, 1, 1, 1, 2)),
            np.array((2, 1, 1, 0, 1, 0)),
            np.array((0, 1, 0, 1, 1, 2)),
            np.array((2, 1, 0, 1, 1, 0)),
            np.array((0, 1, 1, 0, 1, 2)),
        ],
        3,
        1,
    ],
}


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


def change_sequences_to_white():
    sequences = BLACK_SEQUENCES
    for seq_list in sequences.values():
        for i, seq in enumerate(seq_list[0]):
            seq_list[0][i] = np.select(
                [seq == BLACK_VALUE, seq == WHITE_VALUE],
                [WHITE_VALUE, BLACK_VALUE],
                seq,
            )
    return sequences


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
