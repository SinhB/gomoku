import numpy as np
import time

import board_functions
import get_move
import get_lines

def board_four_in_a_row(board):
    board = board_functions.place_stone(board, np.array([4, 6]), 1)
    board = board_functions.place_stone(board, np.array([5, 6]), -1)
    board = board_functions.place_stone(board, np.array([4, 7]), 1)
    board = board_functions.place_stone(board, np.array([5, 8]), -1)
    board = board_functions.place_stone(board, np.array([4, 8]), 1)
    board = board_functions.place_stone(board, np.array([3, 8]), -1)
    # board = board_functions.place_stone(board, np.array([4, 9]), 1)
    # board = board_functions.place_stone(board, np.array([3, 9]), -1)
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

def test_eat_row(board):
    board, total_eat = board_functions.place_stone(board, np.array([4, 6]), 1)
    board, total_eat = board_functions.place_stone(board, np.array([4, 7]), -1)
    board, total_eat = board_functions.place_stone(board, np.array([4, 5]), 1)
    board, total_eat = board_functions.place_stone(board, np.array([4, 4]), -1)
    board_functions.print_board(board)
    input()
    return board, total_eat

def is_array_equal(arr, seq):
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

def check_line_win(arr, seq):
    # Check for sequence in the flatten board
    seq_len = len(seq)
    upper_bound = len(arr) - seq_len + 1
    for i in range(upper_bound):
        
        if is_array_equal(arr[i : i + seq_len], seq):
            return True

    return False

def check_win(board, position, player, total_eat):
    if total_eat >= 5:
        print("Win by eating")
        return True
    row_index = position[0]
    col_index = position[1]

    win_array = (player, player, player, player, player)

    lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    if check_line_win(lr_diags, win_array):
        print("Win by alignment")
        return True
    if check_line_win(rl_diags, win_array):
        print("Win by alignment")
        return True
    if check_line_win(rows, win_array):
        print("Win by alignment")
        return True
    if check_line_win(columns, win_array):
        print("Win by alignment")
        return True
    return False

if __name__ == "__main__":
    board = board_functions.init_board(19)

    start = time.time()
    player = 1
    total_eat = {-1: 0, 1: 0}
    total_time = {-1: 0, 1: 0}

    for i in range(0, 361):
        eat = 0

        one_move_timer = time.time()
        next_move = get_move.get_next_move(board, 19, 5, True, player, total_eat)
        one_move_timer_stop = time.time()
        print(f"Move search time : {one_move_timer_stop - one_move_timer}")
        print(f"SELECTED MOVE : {next_move}")
        total_time[player] += one_move_timer_stop - one_move_timer

        board, eat = board_functions.place_stone(board, next_move, player)
        total_eat[player] += eat

        if check_win(board, next_move, player, total_eat[player]):
            board_functions.print_board(board, next_move)
            print(f"Player {player} ({'B' if player == -1 else 'N'}) won the game with {i} moves played in total during the game")
            print(f"Average time for N : {total_time[1] / (i / 2)}")
            print(f"Average time for B : {total_time[-1] / (i / 2)}")
            break
        board_functions.print_board(board, next_move)

        player = player * -1
        print("---------------------------------------------------------------------\n\n\n\n\n\n")


    print(f"Total : {time.time() - start}")