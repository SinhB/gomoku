
import numpy as np
from numba import njit, prange
from numba.typed import List
from numba.types import int8
from termcolor import colored

from src.utils import timeit

@njit("boolean(int64[:], int64[:])", fastmath=True)
def is_array_equal(arr, seq):
    """Check equality for 2 given arrays
    Arrays should be of same shape

    Parameters
    ----------
    arr      : input 1D array
    seq      : input 1D array
    Output
    ------
    Output    : True if equal else False
    """
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

@njit("UniTuple(int64, 2)(int64[:], int64[:])", fastmath=True)
def numba_search_sequence(arr, seq):
    """Find sequence in an array using NumPy only.

    Parameters
    ----------
    arr      : input 1D array
    seq      : input 1D array
    Output
    ------
    Output    : black_seq number, white_seq number
    """

    black_seq = seq * 1
    white_seq = seq * -1

    # Check for sequence in the flatten board
    black_seq_count = 0
    white_seq_count = 0
    seq_len = seq.size
    upper_bound = arr.size - seq_len + 1
    for i in prange(upper_bound):
        if is_array_equal(arr[i : i + seq_len], black_seq):
            black_seq_count += 1
        if is_array_equal(arr[i : i + seq_len], white_seq):
            white_seq_count += 1

    return black_seq_count, white_seq_count

@njit("int64[:](int64[:,:])", fastmath=True)
def remove_blank_line(array):
    """Remove blank lines and flatten the 2Darray

    Parameters
    ----------
    position  : 2d array
    Output
    ------
    Output    : Flatten non-blank 1d array
    """
    sumrow = np.abs(array).sum(-1)
    array = array[sumrow > 0]

    # Flatten the board with 3 as separator
    Sa = array.shape
    fill = np.full((Sa[0], Sa[1] + 1), 3)
    fill[:, :-1] = array
    flatten_arr = fill.flatten()
    return flatten_arr


@njit("int64[:,:](int64[:,:])", fastmath=True)
def get_diagonals(board) -> np.ndarray:
    """Get diagonals of the current board

    Output
    ------
    Output : 2D Array representing a diagonal on each row.
    """
    
    def _get_diag(b, all_diags):
        for i in range(-19 + 1, 19 - 1):
            di = np.diag(b, k=i)
            d = np.full((1, 19), 3, dtype=np.int64)
            d[-1, : di.shape[0]] = di
            all_diags = np.concatenate((all_diags, d), axis=0)
        return all_diags

    # Pad diag to concatenate them in one ndarray
    all_diags = np.zeros((1, 19), dtype=np.int64)
    all_diags = _get_diag(board, all_diags)
    board = np.flip(np.fliplr(board))
    all_diags = _get_diag(board, all_diags)
        
    return all_diags

@njit(fastmath=True)
def get_sequence_index(index):
    """Get the key name from index in range

    (bisect_left not supported by numba)

    Parameters
    ----------
    position  : index (int)
    Output
    ------
    Output    : name (string)
    """
    max_index = (0, 3, 6, 9, 13, 19, 22, 33, 45)
    for i, value in enumerate(max_index):
        if index <= value:
            return i
    return 0


# @timeit
@njit("int64[:,:](int64[:,:])", fastmath=True, parallel=True)
def get_numba_sequence_frequences(board):
    """Get the frequence of sequences in a board

    Parameters
    ----------
    position  : board (2d array)
    Output
    ------
    Output    : 2d array
    """

    THREAT_PATTERNS = [
        np.array((1, 1, 1, 1, 1), dtype=np.int64),  # Five in a row 100000
        np.array((0, 1, 1, 1, 1, 0), dtype=np.int64),  # OpenFour (4,2)
        np.array((-1, 1, 1, 0, 1, 1, 0, 1, 1, -1), dtype=np.int64),  # OpenFour (4,2)
        np.array((-1, 1, 1, 1, 0, 1, 0, 1, 1, 1, -1), dtype=np.int64),  # OpenFour (4,2)
        np.array((-1, 1, 1, 1, 1, 0), dtype=np.int64),  # SimpleFour (4,1)
        np.array((0, 1, 1, 1, 1, -1), dtype=np.int64),  # SimpleFour (4,1)
        np.array((0, 1, 1, 0, 1, 1, 0), dtype=np.int64),  # SimpleFour (4,1)
        np.array((0, 0, 1, 1, 1, 0, 0), dtype=np.int64),  # OpenThree (3,3)
        np.array((0, 1, 0, 1, 1, 0, 1, 0), dtype=np.int64),  # OpenThree (3,3)
        np.array((1, 0, 1, 0, 1, 0, 1, 0, 1), dtype=np.int64),  # OpenThree (3,3)
        np.array((0, 1, 0, 1, 1, 0), dtype=np.int64),  # BrokenThree (3,2)
        np.array((0, 1, 1, 0, 1, 0), dtype=np.int64),  # BrokenThree (3,2)
        np.array((-1, 0, 1, 1, 1, 0, 0), dtype=np.int64),  # BrokenThree (3,2)
        np.array((0, 0, 1, 1, 1, 0, -1), dtype=np.int64),  # BrokenThree (3,2)
        np.array((-1, 1, 1, 1, 0, 0), dtype=np.int64),  # SimpleThree (3,1)
        np.array((0, 0, 1, 1, 1, -1), dtype=np.int64),  # SimpleThree (3,1)
        np.array((-1, 1, 1, 0, 1, 0), dtype=np.int64),  # SimpleThree (3,1)
        np.array((0, 1, 0, 1, 1, -1), dtype=np.int64),  # SimpleThree (3,1)
        np.array((-1, 1, 0, 1, 1, 0), dtype=np.int64),  # SimpleThree (3,1)
        np.array((0, 1, 1, 0, 1, -1), dtype=np.int64),  # SimpleThree (3,1)
        np.array((0, 0, 1, 1, 0, 0, 0), dtype=np.int64),  # OpenTwo (2,3)
        np.array((0, 0, 1, 0, 1, 0, 0), dtype=np.int64),  # OpenTwo (2,3)
        np.array((0, 0, 0, 1, 1, 0, 0), dtype=np.int64),  # OpenTwo (2,3)
        np.array((0, 1, 0, 0, 1, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 0, 0, 1, 1, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 1, 1, 0, 0, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 1, 0, 1, 0, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 0, 1, 0, 1, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((-1, 0, 0, 1, 1, 0, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((-1, 0, 1, 0, 1, 0, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((-1, 0, 1, 1, 0, 0, 0), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 0, 1, 1, 0, 0, -1), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 0, 1, 0, 1, 0, -1), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((0, 0, 0, 1, 1, 0, -1), dtype=np.int64),  # BrokenTwo (2,2)
        np.array((-1, 0, 1, 1, 0, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((-1, 1, 0, 1, 0, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((-1, 1, 1, 0, 0, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((-1, 1, 0, 0, 1, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((-1, 0, 1, 0, 1, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((-1, 0, 0, 1, 1, 0), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 0, 1, 1, 0, -1), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 0, 1, 0, 1, -1), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 0, 0, 1, 1, -1), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 1, 0, 1, 0, -1), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 1, 0, 0, 1, -1), dtype=np.int64),  # SimpleTwo (2,1)
        np.array((0, 1, 1, 0, 0, -1), dtype=np.int64),  # SimpleTwo (2,1)
    ]

    diags = remove_blank_line(get_diagonals(board))
    rows = remove_blank_line(board)
    columns = remove_blank_line(board.T)

    #First line is BLACK(0), second is WHITE(1) 
    seq_counter_arr = np.zeros((3, 9), dtype=np.int64)
    #number of move to get the next step
    seq_counter_arr[2] = [2, 2, 1, 3, 2, 1, 3, 2, 1]
    
    threat_len = len(THREAT_PATTERNS)
    for i in prange(threat_len):
        seq = THREAT_PATTERNS[i]
        bd, wd = numba_search_sequence(diags, seq)
        br, wr = numba_search_sequence(rows, seq)
        bc, wc = numba_search_sequence(columns, seq)

        seq_idx = get_sequence_index(i)
        seq_counter_arr[0, seq_idx] += (bd + br + bc)
        seq_counter_arr[1, seq_idx] += (wd + wr + wc)

    return seq_counter_arr


@timeit
def display(gamestate):
        """Print the board

        Print the board in the terminal with colors for each stone type
        BLACK = blue
        WHITE = red
        """

        def _color_black_and_white(row: str):
            replacement = {-1: colored(2, "blue"), 1: colored(1, "red")}
            for item, rep in replacement.items():
                row = row.replace(str(item), rep)
            return row

        for row in gamestate.board:
            str_row = "".join(str(row)).translate({ord(char): "" for char in "[,]"})
            str_row = " ".join(str_row.split())
            colored_row = _color_black_and_white(str_row)
            print(colored_row)