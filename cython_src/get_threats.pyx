cimport cython
import numpy as np
cimport numpy as np

import get_lines

def is_array_equal(arr, seq):
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

def get_new_threats(np.ndarray[np.int_t, ndim=2] board, int row_index, int col_index):
    diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    current_threats = get_sequences(diags, rows, columns)

    diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    new_threats = get_sequences(diags, rows, columns)


    # print(current_threats)
    # print(new_threats)
    return new_threats

def numba_search_sequence(arr, seq):
    black_seq = seq * 1
    white_seq = seq * -1

    # Check for sequence in the flatten board
    black_seq_count = 0
    white_seq_count = 0
    seq_len = len(seq)
    upper_bound = len(arr) - len(seq) + 1
    for i in range(upper_bound):
        if is_array_equal(arr[i : i + seq_len], black_seq):
            black_seq_count += 1
        if is_array_equal(arr[i : i + seq_len], white_seq):
            white_seq_count += 1

    return black_seq_count, white_seq_count

def _get_sequence_key_from_index(index):
    max_index = (0, 3, 6, 9, 13, 19, 22, 33, 45)
    keys = (
        "five",
        "open_four",
        "simple_four",
        "open_three",
        "broken_three",
        "simple_three",
        "open_two",
        "broken_two",
        "simple_two",
    )
    for i, value in enumerate(max_index):
        if index <= value:
            return keys[i]
    return "none"

def get_sequences(np.ndarray[np.int_t, ndim=1] diags, np.ndarray[np.int_t, ndim=1] rows, np.ndarray[np.int_t, ndim=1] columns):
    THREAT_PATTERNS = [
        # Five
        np.array((1, 1, 1, 1, 1)),
        # Open four
        np.array((0, 1, 1, 1, 1, 0)),
        np.array((-1, 1, 1, 0, 1, 1, 0, 1, 1, -1)),
        np.array((-1, 1, 1, 1, 0, 1, 0, 1, 1, 1, -1)),
        # Simple four
        np.array((-1, 1, 1, 1, 1, 0)),
        np.array((0, 1, 1, 1, 1, -1)),
        np.array((0, 1, 1, 0, 1, 1, 0)),
        # Open three
        np.array((0, 0, 1, 1, 1, 0, 0)),
        np.array((0, 1, 0, 1, 1, 0, 1, 0)),
        np.array((1, 0, 1, 0, 1, 0, 1, 0, 1)),
        # Broken three
        np.array((0, 1, 0, 1, 1, 0)),
        np.array((0, 1, 1, 0, 1, 0)),
        np.array((-1, 0, 1, 1, 1, 0, 0)),
        np.array((0, 0, 1, 1, 1, 0, -1)),
        # Simple three
        np.array((-1, 1, 1, 1, 0, 0)),
        np.array((0, 0, 1, 1, 1, -1)),
        np.array((-1, 1, 1, 0, 1, 0)),
        np.array((0, 1, 0, 1, 1, -1)),
        np.array((-1, 1, 0, 1, 1, 0)),
        np.array((0, 1, 1, 0, 1, -1)),
        # Open two
        np.array((0, 0, 1, 1, 0, 0, 0)),
        np.array((0, 0, 1, 0, 1, 0, 0)),
        np.array((0, 0, 0, 1, 1, 0, 0)),
        # Broken two
        np.array((0, 1, 0, 0, 1, 0)),
        np.array((0, 0, 0, 1, 1, 0)),
        np.array((0, 1, 1, 0, 0, 0)),
        np.array((0, 1, 0, 1, 0, 0)),
        np.array((0, 0, 1, 0, 1, 0)),
        np.array((-1, 0, 0, 1, 1, 0, 0)),
        np.array((-1, 0, 1, 0, 1, 0, 0)),
        np.array((-1, 0, 1, 1, 0, 0, 0)),
        np.array((0, 0, 1, 1, 0, 0, -1)),
        np.array((0, 0, 1, 0, 1, 0, -1)),
        np.array((0, 0, 0, 1, 1, 0, -1)),
        # Simple two
        np.array((-1, 0, 1, 1, 0, 0)),
        np.array((-1, 1, 0, 1, 0, 0)),
        np.array((-1, 1, 1, 0, 0, 0)),
        np.array((-1, 1, 0, 0, 1, 0)),
        np.array((-1, 0, 1, 0, 1, 0)),
        np.array((-1, 0, 0, 1, 1, 0)),
        np.array((0, 0, 1, 1, 0, -1)),
        np.array((0, 0, 1, 0, 1, -1)),
        np.array((0, 0, 0, 1, 1, -1)),
        np.array((0, 1, 0, 1, 0, -1)),
        np.array((0, 1, 0, 0, 1, -1)),
        np.array((0, 1, 1, 0, 0, -1)),
    ]

    d = {
        "BLACK": {
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
        "WHITE": {
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

    for i, seq in enumerate(THREAT_PATTERNS):
        key = _get_sequence_key_from_index(i)
        bd, wd = numba_search_sequence(diags, seq)
        br, wr = numba_search_sequence(rows, seq)
        bc, wc = numba_search_sequence(columns, seq)
        d["BLACK"][key] += bd + br + bc
        d["WHITE"][key] += wd + wr + wc

    return d
