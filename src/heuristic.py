import numpy as np
from numba import njit

@njit(fastmath=True)
def numba_search_sequence(arr, seq, i):
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
    black_count = 0
    white_count = 0
    flatten_len, seq_len = flatten_arr.size, seq.size
    upper_bound = flatten_len - seq_len + 1
    for i in range(upper_bound):
        if np.array_equal(flatten_arr[i:i+seq_len], black_seq):
            black_count += 1
        if np.array_equal(flatten_arr[i:i+seq_len], white_seq):
            white_count += 1

    return black_count + white_count

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

# @timeit
@njit
def get_numba_sequence_frequences(board, color):
    """Get the frequence of sequences in a board
    """

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



    b = board
    diags = remove_blank_line(get_diagonals(b))
    rows = remove_blank_line(b)
    columns = remove_blank_line(b.T)

    total = 0
    for i, seq in enumerate(NUMBA_SEQUENCE):
        total += numba_search_sequence(diags, seq, i)
        total += numba_search_sequence(rows, seq, i)
        total += numba_search_sequence(columns, seq, i)
    # print(total)
    # return total
    return diags.shape, rows.shape, columns.shape 