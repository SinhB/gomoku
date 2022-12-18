import numpy as np
import numba as nb

from numba import njit, prange, int64, typeof
from numba.types import bool_
from numba.experimental import jitclass

moves = np.array([[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]])

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

@njit
def make_2d(array_list):
    width = len(array_list)
    height = array_list[0].shape[0]
    array_2d = np.zeros((width, height), dtype=np.int64)
    for i in prange(width):
        array_2d[i] = array_list[i]
    return(array_2d)

@njit("int64[:,:](int64[:,:])", fastmath=True)
def remove_oob(arr):
    """Remove position that are out of board"""
    mask = ((arr[:, 0] >= 0) & (arr[:, 0] < 19) & (arr[:, 1] >= 0) & (arr[:, 1] < 19))
    return arr[mask, :]

@njit("int64[:,:](int64[:,:], int64[:,:])", fastmath=True)
def remove_stones(possible_pos, stones):
    """Remove position that already have a stone"""
    mask = np.zeros(possible_pos.shape[0], dtype=bool_)
    lstones = len(stones)
    lpossible_pos = len(possible_pos)
    for i in prange(lpossible_pos):
        found = False
        for j in prange(lstones):
            if is_array_equal(stones[j], possible_pos[i]):
                mask[i] = False
                found = True
        if not found:
            mask[i] = True
    return possible_pos[mask]

@njit("int64[:,:](int64[:,:])", fastmath=True)
def remove_double(possible_pos):
    mask = np.zeros(possible_pos.shape[0], dtype=bool_)
    l = len(possible_pos)
    for i in prange(l):
        found = False
        for j in prange(i + 1, l):
            if is_array_equal(possible_pos[i], possible_pos[j]):
                mask[i] = False
                mask[j] = True
                found = True
        if not found and not mask[i]:
            mask[i] = True
    return possible_pos[mask]

@njit("int64[:,:](int64[:,:])", fastmath=True)
def get_available_pos(board):

    stones = np.concatenate((np.argwhere(board == -1), np.argwhere(board == 1)), axis=0)
    possible_pos = nb.typed.List()
    for i in range(len(stones)):
        for j in range(len(moves)):
            pos = moves[j] + stones[i]
            possible_pos.append(pos)
    np_possible_pos = make_2d(possible_pos)
    np_possible_pos = remove_oob(np_possible_pos)
    np_possible_pos = remove_stones(np_possible_pos, stones)
    np_possible_pos = remove_double(np_possible_pos)
    return np_possible_pos

@njit("UniTuple(int64[:], 2)(int64[:,:], int64, int64)", fastmath=True)
def get_diags(board, row_index, col_index):
    lr_diags = np.diag(board, col_index - row_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    return lr_diags, rl_diags

@njit("UniTuple(int64[:], 4)(int64[:,:], int64, int64)", fastmath=True)
def get_vectors(board, row_index, col_index):
    lr_diags, rl_diags = get_diags(board, row_index, col_index)
    row = board[row_index, :]
    column = board[:, col_index]
    return lr_diags, rl_diags, row, column