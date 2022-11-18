import numpy as np
import time
import itertools

import board_functions
import get_threats
import get_move

def create_cache():
    cache = {}
    possible_values = [-1, 0, 1]
    for i in range(0, 6):
        subset = [x for x in itertools.product(possible_values, repeat=i)]
        # print(subset)
        # print(len(subset))
        for sub in subset:
            cache["MA" + "".join([str(x) for x in sub])] = get_threats.check_side(sub, 1)
            cache["MI" + "".join([str(x) for x in sub])] = get_threats.check_side(sub, -1)
    print(cache.keys())
    print(len(cache.keys()))
    return cache

def board_four_in_a_row(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 7]), 1)
    board = board_functions.place_stone(board, np.array([5, 8]), -1)
    board = board_functions.place_stone(board, np.array([4, 8]), 1)
    # board = board_functions.place_stone(board, np.array([4, 9]), 1)
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
    board = board_functions.place_stone(board, np.array([4, 3]), -1)
    board = board_functions.place_stone(board, np.array([5, 2]), 1)
    board = board_functions.place_stone(board, np.array([7, 7]), -1)
    board = board_functions.place_stone(board, np.array([8, 9]), 1)
    board = board_functions.place_stone(board, np.array([7, 9]), -1)
    board = board_functions.place_stone(board, np.array([9, 9]), 1)
    board = board_functions.place_stone(board, np.array([8, 7]), -1)
    board = board_functions.place_stone(board, np.array([4, 5]), 1)
    return board

if __name__ == "__main__":
    board = board_functions.init_board(19)

    # board = simple_board(board)
    board = complex_board(board)
    # board = board_four_in_a_row(board)
    # start_cache = time.time()
    # cache = create_cache()
    # print(f"Create cache time : {time.time() - start_cache}")

    print(board)
    start = time.time()
    maximizing_player = True
    # maximizing_player = False
    for i in range(0, 10):
        one_move_timer = time.time()
        next_move = get_move.get_next_move(board, 19, 6, maximizing_player)
        print(f"SELECTED MOVE : {next_move}")
        board = board_functions.place_stone(board, next_move, 1 if maximizing_player else -1)
        print(f"Move search time : {time.time() - one_move_timer}")
        print(board)
        maximizing_player = not maximizing_player


    print(f"Total : {time.time() - start}")