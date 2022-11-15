import board_functions
import get_move
import numpy as np
import time

def board_four_in_a_row(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 7]), 1)
    board = board_functions.place_stone(board, np.array([4, 8]), 1)
    board = board_functions.place_stone(board, np.array([4, 9]), 1)
    return board

def simple_board(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 7]), 1)
    return board

def complex_board(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 4]), 1)
    board = board_functions.place_stone(board, np.array([0, 0]), -1)
    board = board_functions.place_stone(board, np.array([1, 1]), 1)
    board = board_functions.place_stone(board, np.array([4, 3]), -1)
    board = board_functions.place_stone(board, np.array([5, 2]), 1)
    board = board_functions.place_stone(board, np.array([7, 7]), -1)
    board = board_functions.place_stone(board, np.array([4, 5]), 1)
    return board

if __name__ == "__main__":
    board = board_functions.init_board(19)

    # board = simple_board(board)
    board = complex_board(board)
    # board = board_four_in_a_row(board)

    print(board)
    start = time.time()
    get_move.get_next_move(board, 19, 7)
    print(f"Total : {time.time() - start}")