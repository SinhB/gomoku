#!python
#cython: language_level=3
import board_functions
import get_move
import numpy as np
import time


if __name__ == "__main__":
    board = board_functions.init_board(19)

    board = board_functions.place_stone(board, np.array([4, 4]), 1)
    # board = board_functions.place_stone(board, np.array([0, 0]), -1)
    # board = board_functions.place_stone(board, np.array([1, 1]), 1)
    # board = board_functions.place_stone(board, np.array([4, 3]), -1)
    # board = board_functions.place_stone(board, np.array([5, 2]), 1)
    board = board_functions.place_stone(board, np.array([7, 7]), -1)
    board = board_functions.place_stone(board, np.array([4, 5]), 1)
    print(board)
    start = time.time()
    get_move.get_next_move(board, 19, 3)
    print(f"Total : {time.time() - start}")