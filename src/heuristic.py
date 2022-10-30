from bisect import bisect_left
from copy import deepcopy
import numpy as np
from numba import njit, jit, typeof
from numba.core import types
from numba.typed import Dict

from src.utils import Color, timeit

@njit(fastmath=True)
def numba_search_sequence(arr, seq, sequence_index):
    """Find sequence in an array using NumPy only.

    Parameters
    ----------
    arr      : input 2D array
    seq      : input 1D array
    seq_type : name of the sequence
    seq_list : score associate to the sequence type
    """

    black_seq = seq * 1
    white_seq = seq * -1

    # Flatten the board with 3 as separator
    Sa = arr.shape
    fill = np.full((Sa[0], Sa[1] + 1), 3)
    fill[:,:-1] = arr
    flatten_arr = fill.flatten()

    # Check for sequence in the flatten board
    black_seq_count = 0
    white_seq_count = 0
    flatten_len, seq_len = flatten_arr.size, seq.size
    upper_bound = flatten_len - seq_len + 1
    for i in range(upper_bound):
        if np.array_equal(flatten_arr[i:i+seq_len], black_seq):
            black_seq_count += 1
        if np.array_equal(flatten_arr[i:i+seq_len], white_seq):
            white_seq_count += 1

    return black_seq_count, white_seq_count

@njit(fastmath=True)
def remove_blank_line(array):
    """
    """
    sumrow = np.abs(array).sum(-1)
    array = array[sumrow > 0]
    return array


@njit('int8[:,:](int8[:,:])', fastmath=True)
def get_diagonals(board) -> np.ndarray:
    """Get diagonals of the current board

    Output
    ------
    Output : 2D Array representing a diagonal on each row.
    """

    def _get_diag(b, shape, d_list=[]):
        for i in range(-shape+1, shape-1):
            d = np.diag(b, k=i)
            d_list.append(d)
        return d_list

    shape = board.shape[0]
    diag_list = _get_diag(board, shape)
    #flip to get others diags
    board = np.flip(np.fliplr(board))
    diag_list = _get_diag(board, shape, diag_list)

    max_len = 0
    for i in range(len(diag_list)):
        if diag_list[i].size > max_len:
            max_len = diag_list[i].size

    # Pad diag to concatenate them in one ndarray
    all_diags = np.zeros((1, max_len), dtype=np.int8)
    for diag in diag_list:
        d = np.full((1, max_len), 0, dtype=np.int8)
        d[-1, :diag.shape[0]] = diag
        all_diags = np.concatenate((all_diags, d), axis=0)

    return all_diags

@timeit
# @njit
def get_numba_sequence_frequences(board, color):
    """Get the frequence of sequences in a board
    """

    def _get_sequence_key_from_index(index):
        max_index = [0, 3, 6, 9, 13, 19, 22, 33, 45]
        keys = ["five", "open_four", "simple_four", "open_three", "broken_three", "simple_three", "open_two", "broken_two", "simple_two"]
        i = bisect_left(max_index, index)
        return keys[i]

    NUMBA_SEQUENCE = [
        np.array((1, 1, 1, 1, 1)), #Five in a row 100000

        np.array((0, 1, 1, 1, 1, 0)), #OpenFour (4,2)
        np.array((-1, 1, 1, 0, 1, 1, 0, 1, 1, -1)), #OpenFour (4,2)
        np.array((-1, 1, 1, 1, 0, 1, 0, 1, 1, 1, -1)), #OpenFour (4,2)

        np.array((-1, 1, 1, 1, 1, 0)), #SimpleFour (4,1)
        np.array((0, 1, 1, 1, 1, -1)), #SimpleFour (4,1)
        np.array((0, 1, 1, 0, 1, 1, 0)), #SimpleFour (4,1)

        np.array((0, 0, 1, 1, 1, 0, 0)), #OpenThree (3,3)
        np.array((0, 1, 0, 1, 1, 0, 1, 0)), #OpenThree (3,3)
        np.array((1, 0, 1, 0, 1, 0, 1, 0, 1)), #OpenThree (3,3)

        np.array((0, 1, 0, 1, 1, 0)), #BrokenThree (3,2)
        np.array((0, 1, 1, 0, 1, 0)), #BrokenThree (3,2)
        np.array((-1, 0, 1, 1, 1, 0, 0)), #BrokenThree (3,2)
        np.array((0, 0, 1, 1, 1, 0, -1)), #BrokenThree (3,2)

        np.array((-1, 1, 1, 1, 0, 0)), #SimpleThree (3,1)
        np.array((0, 0, 1, 1, 1, -1)), #SimpleThree (3,1)
        np.array((-1, 1, 1, 0, 1, 0)), #SimpleThree (3,1)
        np.array((0, 1, 0, 1, 1, -1)), #SimpleThree (3,1)
        np.array((-1, 1, 0, 1, 1, 0)), #SimpleThree (3,1)
        np.array((0, 1, 1, 0, 1, -1)), #SimpleThree (3,1)

        np.array((0, 0, 1, 1, 0, 0, 0)), #OpenTwo (2,3)
        np.array((0, 0, 1, 0, 1, 0, 0)), #OpenTwo (2,3)
        np.array((0, 0, 0, 1, 1, 0, 0)), #OpenTwo (2,3)

        np.array((0, 1, 0, 0, 1, 0)), #BrokenTwo (2,2)
        np.array((0, 0, 0, 1, 1, 0)), #BrokenTwo (2,2)
        np.array((0, 1, 1, 0, 0, 0)), #BrokenTwo (2,2)
        np.array((0, 1, 0, 1, 0, 0)), #BrokenTwo (2,2)
        np.array((0, 0, 1, 0, 1, 0)), #BrokenTwo (2,2)
        np.array((-1, 0, 0, 1, 1, 0, 0)), #BrokenTwo (2,2)
        np.array((-1, 0, 1, 0, 1, 0, 0)), #BrokenTwo (2,2)
        np.array((-1, 0, 1, 1, 0, 0, 0)), #BrokenTwo (2,2)
        np.array((0, 0, 1, 1, 0, 0, -1)), #BrokenTwo (2,2)
        np.array((0, 0, 1, 0, 1, 0, -1)), #BrokenTwo (2,2)
        np.array((0, 0, 0, 1, 1, 0, -1)), #BrokenTwo (2,2)

        np.array((-1, 0, 1, 1, 0, 0)), #SimpleTwo (2,1)
        np.array((-1, 1, 0, 1, 0, 0)), #SimpleTwo (2,1)
        np.array((-1, 1, 1, 0, 0, 0)), #SimpleTwo (2,1)
        np.array((-1, 1, 0, 0, 1, 0)), #SimpleTwo (2,1)
        np.array((-1, 0, 1, 0, 1, 0)), #SimpleTwo (2,1)
        np.array((-1, 0, 0, 1, 1, 0)), #SimpleTwo (2,1)
        np.array((0, 0, 1, 1, 0, -1)), #SimpleTwo (2,1)
        np.array((0, 0, 1, 0, 1, -1)), #SimpleTwo (2,1)
        np.array((0, 0, 0, 1, 1, -1)), #SimpleTwo (2,1)
        np.array((0, 1, 0, 1, 0, -1)), #SimpleTwo (2,1)
        np.array((0, 1, 0, 0, 1, -1)), #SimpleTwo (2,1)
        np.array((0, 1, 1, 0, 0, -1)), #SimpleTwo (2,1)
    ]

    dict_value = {
        "five": 0,
        "open_four": 0,
        "simple_four": 0,
        "open_three": 0,
        "broken_three": 0,
        "simple_three": 0,
        "open_two": 0,
        "broken_two": 0,
        "simple_two": 0,
    }
    
    d = {Color.BLACK.name: dict_value.copy(), Color.WHITE.name: dict_value.copy()}

    b = board
    diags = remove_blank_line(get_diagonals(b))
    rows = remove_blank_line(b)
    columns = remove_blank_line(b.T)

    for i, seq in enumerate(NUMBA_SEQUENCE):
        key = _get_sequence_key_from_index(i)
        bd, wd = numba_search_sequence(diags, seq, i)
        br, wr = numba_search_sequence(rows, seq, i)
        bc, wc = numba_search_sequence(columns, seq, i)
        d[Color.BLACK.name][key] += (bd + br + bc)
        d[Color.WHITE.name][key] += (wd + wr + wc)

    return d