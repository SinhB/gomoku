# #!python
# #cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np

ctypedef np.int_t DTYPE_t

def get_available_positions(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef np.ndarray[np.int_t, ndim=2] moves
    cdef np.ndarray[np.int_t, ndim=2] possible_moves
    cdef np.ndarray[np.uint8_t, ndim=1, cast=True] in_board

    all_stones = np.argwhere(board != 0)
    moves = np.array([[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]])
    possible_pos = np.vstack(all_stones + moves[:, None])
    in_board = (
        (possible_pos[:, 0] >= 0)
        & (possible_pos[:, 0] < size)
        & (possible_pos[:, 1] >= 0)
        & (possible_pos[:, 1] < size)
    )
    possible_pos = possible_pos[in_board, :]
    possible_pos = np.unique(
        possible_pos[
            np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
        ],
        axis=0,
    )
    return possible_pos

def remove_blank_line(array):
    # cdef np.ndarray[np.int_t, ndim=1] flatten_arr
    sumrow = np.abs(array).sum(1)
    array = array[sumrow > 0]

    # Flatten the board with 3 as separator
    Sa = array.shape
    fill = np.full((Sa[0], Sa[1] + 1), 3)
    fill[:, :-1] = array
    flatten_arr = fill.flatten()
    return flatten_arr

@cython.boundscheck(False)
@cython.wraparound(False)
def _get_diag(np.ndarray[np.int_t, ndim=2] b, int size, d_list=[]):
    cdef int i

    for i in range(-size + 1, size - 1):
        d_list.append(np.diag(b, k=i))
    return d_list

@cython.boundscheck(False)
@cython.wraparound(False)
def get_diagonals(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef l
    cdef np.ndarray[np.int_t, ndim=2] diagonals
    # cdef np.ndarray[np.int_t, ndim=1] diag_list

    diag_list = _get_diag(board, size)
    # flip to get others diags
    board = np.flip(np.fliplr(board))
    diag_list = _get_diag(board, size, diag_list)

    max_len = 0
    for i in range(len(diag_list)):
        if diag_list[i].size > max_len:
            max_len = diag_list[i].size

    # Pad diag to concatenate them in one ndarray
    all_diags = np.zeros((1, max_len), dtype=np.int8)
    for diag in diag_list:
        d = np.full((1, max_len), 0, dtype=np.int8)
        d[-1, : diag.shape[0]] = diag
        all_diags = np.concatenate((all_diags, d), axis=0)

    return remove_blank_line(all_diags)


def get_rows(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef int i
    rows = []
    for i in range(size):
        tmp = board[i].tolist()
        if np.any(board[i]):
            tmp.append(3)
            rows += tmp
    return np.array(rows)
