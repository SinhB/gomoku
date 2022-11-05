#!python
#cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np

import get_lines

ctypedef np.int_t DTYPE_t
@cython.boundscheck(False)
@cython.wraparound(False)
def get_next_move(
    np.ndarray[np.int_t, ndim=2] board,
    int size,
    int depth
):

    cdef int alpha
    cdef int beta
    cdef bint maximizing_player

    alpha = -100000000
    beta = 100000000
    maximizing_player = True
    available_pos = get_lines.get_available_positions(board, size)
    # good_pos = sort_moves(available_pos, maximizing_player, 10)
    best_position = available_pos[0]
    score = -100000000


    diags = get_lines.get_diagonals(board, size)
    rows = get_lines.get_rows(board, size)
    columns = get_lines.get_rows(board.T, size)
    current_threats = get_sequences(diags, rows, columns)

    for position in available_pos:
        print(position)
        board[position[0]][position[1]] = 1
        # print(get_lines.get_new_threats(board, position))
        next_move = minimax(board, depth, alpha, beta, maximizing_player, size, current_threats)
        # print("Next move:")
        print(next_move)
        board[position[0]][position[1]] = 0
    return 5

def evaluate(np.ndarray[np.int_t, ndim=2] board, int size, current_threats, str color):
    print("Evaluate")
    print(current_threats)
    
    diags = get_lines.get_diagonals(board, size)
    rows = get_lines.get_rows(board, size)
    columns = get_lines.get_rows(board.T, size)
    current_threats = get_sequences(diags, rows, columns)

    priority_keys = (
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

    # Get the first 'counter' type of sequence to make the score
    counter = 2
    score = 0
    for i, key in enumerate(priority_keys):
        if counter == 0:
            return score
        if current_threats[color][key] != 0:
            counter -= 1
            score += 9 - i * current_threats[color][key]
    return score


def minimax(
    np.ndarray[np.int_t, ndim=2] board,
    int depth,
    int alpha,
    int beta,
    bint maximizing_player,
    int size,
    current_threats
):
    # if depth == 0 or is_finished():
    if depth == 0:
        # return evaluate(board, size, current_threats, "WHITE")
        return evaluate(board, size, current_threats, "BLACK")
    available_pos = get_lines.get_available_positions(board, size)
    # print(available_pos)
    if maximizing_player:
        maxEval = -10000000
        for position in available_pos:
            board[position[0]][position[1]] = 1
            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, current_threats)
            board[position[0]][position[1]] = 0

            maxEval = max(alpha, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 10000000
        for position in available_pos:
            board[position[0]][position[1]] = -1
            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, current_threats)
            board[position[0]][position[1]] = 0

            minEval - min(beta, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def is_array_equal(arr, seq):
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

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
