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

def board_four_in_a_row(b_board, n_board):
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 6])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [5, 6])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 7])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [5, 8])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 8])
    return b_board, n_board

def simple_board(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 7]), 1)
    return board

def complex_board(b_board, n_board):
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 6])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [5, 6])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 4])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [4, 3])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [5, 2])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [7, 7])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [8, 9])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [7, 9])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [9, 9])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [8, 7])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [4, 5])
    b_board, n_board = board_functions.place_stone(b_board, n_board, [6, 6])
    n_board, b_board = board_functions.place_stone(n_board, b_board, [2, 2])
    print(n_board)
    print(b_board)
    return b_board, n_board

if __name__ == "__main__":
    b_board, n_board = board_functions.init_board(19)
    print(bin(n_board))
    print(len(bin(n_board)))
    # board = simple_board(board)
    # b_board, n_board = complex_board(b_board, n_board)
    # b_board, n_board = board_four_in_a_row(b_board, n_board)
    # start_cache = time.time()
    # cache = create_cache()
    # print(f"Create cache time : {time.time() - start_cache}")
    board_functions.print_board(b_board, n_board)

    start = time.time()
    player = 'noir'
    for i in range(0, 10):
        one_move_timer = time.time()
        if player == 'noir':
            next_move = get_move.get_next_move(b_board, n_board, 19, 8)
            print(f"SELECTED MOVE : {next_move}")
            n_board[next_move] = 1
            player = 'blanc'

        else:
            next_move = get_move.get_next_move(n_board, b_board, 19, 8)
            b_board[next_move] = 1
            print(f"SELECTED MOVE : {next_move}")
            player = 'noir'

        board_functions.print_board(b_board, n_board)
        print(f"Move search time : {time.time() - one_move_timer}")


    print(f"Total : {time.time() - start}")