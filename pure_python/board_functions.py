import numpy as np


def init_board(size):
    board = np.zeros([size, size], dtype=np.int)
    return board

def place_stone(board, position, color):
    board[position[0]][position[1]] = color
    return board

def remove_stone(board, position, color):
    board[position[0]][position[1]] = 0
    return board
