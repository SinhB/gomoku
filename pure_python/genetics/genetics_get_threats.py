import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_
import json
# from check_lines import check_line

# multiplicator_five = 11_000
# multiplicator_open_four = 1_490
# multiplicator_open_three = 1_450
# multiplicator_semi_closed_four = 500
# multiplicator_semi_closed_three = 390
# multiplicator_open_two = 1
# multiplicator_semi_close_two = 0

# @njit("(int64)(int64)", fastmath=True)
# def eat_value(eat_number):
#     if eat_number >= 5:
#         return 100_000
#     if eat_number == 4:
#         return 1_400
#     if eat_number == 3:
#         return 1_100
#     if eat_number == 2:
#         return 1_050
#     return 1_000

with open('hash_table.json') as f:
    hash_table = json.load(f)


def check_line(line, starting_index, player):
    return hash_table[hash((line.tobytes(), starting_index, player))]

@njit("UniTuple(boolean, 4)(int64[:], int64)")
def check_vulnerability(side, player):
    is_consec = True
    consec = 0

    for i in range(0, min(len(side), 2)):
        if side[i] == 0:
            if i == 0:
                return False, True, False, False
            if i == 1 and consec == 1:
                return False, False, False, True
            else:
                is_consec = False
        if side[i] == player:
            if is_consec:
                consec += 1
        if side[i] == -player:
            if i == 0:
                return True, False, False, False
            if i == 1 and consec == 1:
                return False, False, True, False
            else:
                is_consec = False
    return False, False, False, False

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

@njit("boolean(boolean, int64)", fastmath=True)
def five_and_enemy_capture(five, enemy_total_eat):
    if five and enemy_total_eat == 4:
        return True
    return False

@njit("int64[:](boolean, int64, int64, int64, int64)")
def get_pos(is_left, index, row_index, col_index, line_type):
    """
        0: LR
        1: RL
        2: ROW
        3: COL
        return: (row, col)
    """
    if is_left:
        if line_type == 0:
            return np.array((row_index - index, col_index - index))
        if line_type == 1:
            return np.array((row_index - index, col_index + index))
        if line_type == 2:
            return np.array((row_index, col_index - index))
        if line_type == 3:
            return np.array((row_index - index, col_index))
    else:
        if line_type == 0:
            return np.array((row_index + index, col_index + index))
        if line_type == 1:
            return np.array((row_index + index, col_index - index))
        if line_type == 2:
            return np.array((row_index, col_index + index))
        if line_type == 3:
            return np.array((row_index + index, col_index))
    return np.zeros(2, dtype=np.int64)


@njit("Tuple((boolean, boolean, int64))(int64[:], int64, int64)", fastmath=True)
def check_line_breakable(line, starting_index, player):
    """Return: (is_breakable, is_left)"""
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]

    l_starting_op, l_starting_blank, l_ending_op, l_ending_blank = check_vulnerability(left, player)
    r_starting_op, r_starting_blank, r_ending_op, r_ending_blank = check_vulnerability(right, player)

    #right
    if l_starting_op and r_ending_blank:
        return True, False, 2
    if r_starting_blank and l_ending_op:
        return True, False, 1
    #left
    if r_starting_op and l_ending_blank:
        return True, True, 2
    if l_starting_blank and r_ending_op:
        return True, True, 1

    return False, False, 0

@njit("Tuple((boolean, int64[:]))(int64[:,:], int64[:], int64)", fastmath=True)
def pos_is_breakable(board, position, player):
    row_index, col_index = position
    lr_diags, rl_diags, row, column = get_vectors(board, row_index, col_index)

    lr_starting_index = col_index if row_index > col_index else row_index
    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index

    is_breakable, is_left, index = check_line_breakable(lr_diags, lr_starting_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 0)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(rl_diags, rl_starting_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 1)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(row, col_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 2)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(column, row_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 3)
        return True, pos
    return False, np.zeros(2, dtype=np.int64)


@njit("Tuple((boolean, int64[:]))(int64[:,:], int64, int64[:], int64, int64, int64, int64)", fastmath=True)
def check_if_breakable(board, line_type, line, starting_index, player, row_index, col_index):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    pos_list = [np.array((row_index, col_index))]
    for i in range(0, min(len(left), 6)):
        if left[i] == player:
            new_pos = get_pos(True, i + 1, row_index, col_index, line_type)
            pos_list.append(new_pos)
        else:
            break
    for i in range(0, min(len(right), 6)):
        if right[i] == player:
            new_pos = get_pos(False, i + 1, row_index, col_index, line_type)
            pos_list.append(new_pos)
        else:
            break
    numba_pos_list = nb.typed.List(pos_list)
    for pos in numba_pos_list:
        is_breakable, breaking_pos = pos_is_breakable(board, pos, player)
        if is_breakable:
            return True, breaking_pos
    return False, np.zeros(2, dtype=np.int64)

@njit
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth, eat_multiplicators, multiplicators):
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position
    lr_diags, rl_diags, row, column = get_vectors(board, row_index, col_index)
    
    captured_stones = []

    defend_breaking_five = 0

    lr_starting_index = col_index if row_index > col_index else row_index
    # has_empty_lr, capture_left_lr, capture_right_lr, closed_two_lr, semi_closed_two_lr, open_two_lr, closed_three_lr, semi_closed_three_lr, open_three_lr, closed_four_lr, semi_closed_four_lr, open_four_lr, five_lr = check_line(lr_diags, lr_starting_index, player)
    
    result_lr, five_lr, open_three_lr, capture_left_lr, capture_right_lr = hash_table[hash((lr_diags.tobytes(), lr_starting_index, player))]
    print("OK")
    # result_lr, five_lr, open_three_lr, capture_left_lr, capture_right_lr = check_line(lr_diags, lr_starting_index, player)
    
    if five_and_enemy_capture(five_lr, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(0), lr_diags, lr_starting_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = multiplicators[7]
            # defend_breaking_five = 10_000
    # result_lr = get_score(has_empty_lr, semi_closed_two_lr, open_two_lr, semi_closed_three_lr, open_three_lr, semi_closed_four_lr, open_four_lr, five_lr)
    # result_lr = get_score(has_empty_lr, semi_closed_two_lr, open_two_lr, semi_closed_three_lr, open_three_lr, semi_closed_four_lr, open_four_lr, five_lr, multiplicators[0], multiplicators[1], multiplicators[3], multiplicators[2], multiplicators[4], multiplicators[5], multiplicators[6])

    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
    # has_empty_rl, capture_left_rl, capture_right_rl, closed_two_rl, semi_closed_two_rl, open_two_rl, closed_three_rl, semi_closed_three_rl, open_three_rl, closed_four_rl, semi_closed_four_rl, open_four_rl, five_rl = check_line(rl_diags, rl_starting_index, player)
    result_rl, five_rl, open_three_rl, capture_left_rl, capture_right_rl = hash_table[hash((rl_diags.tobytes(), rl_starting_index, player))]
    # result_rl, five_rl, open_three_rl, capture_left_rl, capture_right_rl = check_line(rl_diags, rl_starting_index, player)
    if five_and_enemy_capture(five_rl, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(1), rl_diags, rl_starting_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = multiplicators[7]
            # defend_breaking_five = 10_000
    # result_rl = get_score(has_empty_rl, semi_closed_two_rl, open_two_rl, semi_closed_three_rl, open_three_rl, semi_closed_four_rl, open_four_rl, five_rl)
    # result_rl = get_score(has_empty_rl, semi_closed_two_rl, open_two_rl, semi_closed_three_rl, open_three_rl, semi_closed_four_rl, open_four_rl, five_rl, multiplicators[0], multiplicators[1], multiplicators[3], multiplicators[2], multiplicators[4], multiplicators[5], multiplicators[6])

    # has_empty_row, capture_left_row, capture_right_row, closed_two_row, semi_closed_two_row, open_two_row, closed_three_row, semi_closed_three_row, open_three_row, closed_four_row, semi_closed_four_row, open_four_row, five_row = check_line(row, col_index, player)
    result_row, five_row, open_three_row, capture_left_row, capture_right_row  = hash_table[hash((row.tobytes(), col_index, player))]
    # result_row, five_row, open_three_row, capture_left_row, capture_right_row = check_line(row, col_index, player)
    if five_and_enemy_capture(five_row, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(2), row, col_index, player, row_index,col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = multiplicators[7]
            # defend_breaking_five = 10_000
    # result_row = get_score(has_empty_row, semi_closed_two_row, open_two_row, semi_closed_three_row, open_three_row, semi_closed_four_row, open_four_row, five_row)
    # result_row = get_score(has_empty_row, semi_closed_two_row, open_two_row, semi_closed_three_row, open_three_row, semi_closed_four_row, open_four_row, five_row, multiplicators[0], multiplicators[1], multiplicators[3], multiplicators[2], multiplicators[4], multiplicators[5], multiplicators[6])

    # has_empty_col, capture_left_col,capture_right_col, closed_two_col, semi_closed_two_col, open_two_col, closed_three_col, semi_closed_three_col, open_three_col, closed_four_col, semi_closed_four_col, open_four_col, five_col = check_line(column, row_index, player)
    result_col, five_col, open_three_col, capture_left_col, capture_right_col = hash_table[hash((column.tobytes(), row_index, player))]
    # result_col, five_col, open_three_col, capture_left_col, capture_right_col = check_line(column, row_index, player)
    if five_and_enemy_capture(five_col, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(3), column, row_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = multiplicators[7]
            # defend_breaking_five = 10_000
    # result_col = get_score(has_empty_col, semi_closed_two_col, open_two_col, semi_closed_three_col, open_three_col, semi_closed_four_col, open_four_col, five_col)
    # result_col = get_score(has_empty_col, semi_closed_two_col, open_two_col, semi_closed_three_col, open_three_col, semi_closed_four_col, open_four_col, five_col, multiplicators[0], multiplicators[1], multiplicators[3], multiplicators[2], multiplicators[4], multiplicators[5], multiplicators[6])

    score = max(result_lr, result_rl, result_row, result_col)

    eat_move = 0
    if capture_left_lr:
        eat_move += 1
    if capture_left_rl:
        eat_move += 1
    if capture_left_row:
        eat_move += 1 
    if capture_left_col:
        eat_move += 1
    if capture_right_lr:
        eat_move += 1
    if capture_right_rl:
        eat_move += 1
    if capture_right_row:
        eat_move += 1
    if capture_right_col:
        eat_move += 1

    adding_eat = 0
    if eat_move:
        total_eat = eat_move + player_eat
        adding_eat = eat_multiplicators[eat_move] if eat_move < 5 else eat_multiplicators[4]

    score = score + adding_eat + defend_breaking_five

    #Fill captured list
    if capture_left_lr:
        captured_left_lr_one = np.array((row_index-1, col_index-1), dtype=int64)
        captured_left_lr_two = np.array((row_index-2, col_index-2), dtype=int64)
        captured_stones.extend([captured_left_lr_one, captured_left_lr_two])
    if capture_right_lr:
        captured_right_lr_one = np.array((row_index+1, col_index+1), dtype=int64)
        captured_right_lr_two = np.array((row_index+2, col_index+2), dtype=int64)
        captured_stones.extend([captured_right_lr_one, captured_right_lr_two])

    if capture_left_rl:
        captured_left_rl_one = np.array((row_index-1, col_index+1), dtype=int64)
        captured_left_rl_two = np.array((row_index-2, col_index+2), dtype=int64)
        captured_stones.extend([captured_left_rl_one, captured_left_rl_two])
    if capture_right_rl:
        captured_right_rl_one = np.array((row_index+1, col_index-1), dtype=int64)
        captured_right_rl_two = np.array((row_index+2, col_index-2), dtype=int64)
        captured_stones.extend([captured_right_rl_one, captured_right_rl_two])

    if capture_left_row:
        captured_left_row_one = np.array((row_index, col_index-1), dtype=int64)
        captured_left_row_two = np.array((row_index, col_index-2), dtype=int64)
        captured_stones.extend([captured_left_row_one, captured_left_row_two])
    if capture_right_row:

        captured_right_row_one = np.array((row_index, col_index+1), dtype=int64)
        captured_right_row_two = np.array((row_index, col_index+2), dtype=int64)
        captured_stones.extend([captured_right_row_one, captured_right_row_two])

    if capture_left_col:
        captured_left_col_one = np.array((row_index-1, col_index), dtype=int64)
        captured_left_col_two = np.array((row_index-2, col_index), dtype=int64)
        captured_stones.extend([captured_left_col_one, captured_left_col_two])
    if capture_right_col:
        captured_right_col_one = np.array((row_index+1, col_index), dtype=int64)
        captured_right_col_two = np.array((row_index+2, col_index), dtype=int64)
        captured_stones.extend([captured_right_col_one, captured_right_col_two])


    is_win = True if eat_move + player_eat == 5 or five_lr or five_rl or five_row or five_col else False
    is_forbidden = True if open_three_lr + open_three_rl + open_three_row + open_three_col >= 2 else False

    if not maximizing_player:
        score *= -1

    return position, score / depth, captured_stones, is_win, is_forbidden, eat_move