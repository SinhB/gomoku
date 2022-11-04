#!python
#cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np


ctypedef np.int_t DTYPE_t
def init_board(int size):
    cdef np.ndarray[np.int_t, ndim=2] board
    board = np.zeros([size, size], dtype=np.int)
    return board

def place_stone(
    np.ndarray[np.int_t, ndim=2] board,
    np.ndarray[np.int_t, ndim=1] position,
    int color
):
    board[position[0]][position[1]] = color
    return board

def remove_stone(np.ndarray[np.int_t, ndim=2] board, position, int color):
    board[position[0]][position[1]] = 0
    return board

# # @cython.language_level("3")
# def get_next_move(board, depth):
#     return get_move.get_sequences(board)
