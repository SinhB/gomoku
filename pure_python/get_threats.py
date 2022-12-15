import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_

multiplicator_five = 10_000
multiplicator_open_four = 1_490
multiplicator_semi_closed_four = 500
multiplicator_open_three = 1_200
multiplicator_semi_closed_three = 400
multiplicator_open_two = 1
multiplicator_semi_close_two = 0

multiplicator_enemy_five = 3_000
multiplicator_enemy_open_four = 1_450
multiplicator_enemy_semi_closed_four = 1_400
multiplicator_enemy_open_three = 1_300
multiplicator_enemy_semi_closed_three = 900
multiplicator_enemy_open_two = 1
multiplicator_enemy_semi_close_two = 1

@njit("(int64)(int64)", fastmath=True)
def eat_value(eat_number):
    if eat_number == 5:
        return 100_000
    return 1_000

@njit("Tuple((int64, int64, boolean, boolean, boolean, boolean, boolean, boolean))(int64[:], int64, boolean)", fastmath=True)
def check_side(side, player, eating=False):
    consec = 0
    consec_op = 0
    additional = 0
    is_after_blank = False
    is_consec = True
    is_additional = True
    check_eating = True
    starting_blank = False
    starting_op = False
    closing_blank = False
    closing_op = False
    could_get_eat = False
    
    for i in range(0, min(len(side), 6)):
        if side[i] == player:
            if check_eating and consec_op == 2:
                eating = True
                new_side = np.copy(side)
                new_side[i-1] = 0
                new_side[i-2] = 0
                return check_side(new_side, player, eating=True)
            check_eating = False
            if not consec_op:
                if is_consec:
                    consec += 1
                else:
                    additional += 1
        if side[i] == 0:
            check_eating = False
            if i == 0:
                starting_blank = True
            if i == 1 and consec == 1:
                could_get_eat = True
            if is_after_blank or consec_op:
                if consec_op and not eating:
                    closing_op = True
                else:
                    closing_blank = True
                break
            is_after_blank = True
            is_consec = False
        if side[i] == -player:
            if i == 0:
                starting_op = True
            if is_after_blank:
                if not additional:
                    closing_blank = True
                else:
                    closing_op = True
                break
            consec_op += 1
            is_consec = False
    if is_after_blank and side[i] != 1 and side[i] != -player:
        closing_blank = True
    else:
        closing_op = True
    return consec, additional, eating, starting_blank, starting_op, closing_blank, closing_op, could_get_eat


@njit("Tuple((boolean, boolean, boolean, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64))(int64[:], int64, int64)", fastmath=True)
def check_line(line, starting_index, player):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    
    l_consec, l_additional, l_eating, l_starting_blank, l_starting_op, l_closing_blank, l_closing_op, l_could_get_eat = check_side(left, player, False)
    r_consec, r_additional, r_eating, r_starting_blank, r_starting_op, r_closing_blank, r_closing_op, r_could_get_eat = check_side(right, player, False)
    
    close_threat = False
    semi_close = False
    open_threat = False
    
    if l_closing_op and r_closing_op:
        close_threat = True
    elif (l_closing_op and not r_closing_op) or (not l_closing_op and r_closing_op):
        semi_close = True
    else:
        open_threat = True
    # print(close_threat, semi_close, open_threat)
    
    total_consec = l_consec + r_consec
    
     # Player serie
    closed_two = 0
    semi_closed_two = 0
    open_two = 0

    closed_three = 0
    semi_closed_three = 0
    open_three = 0

    closed_four = 0
    semi_closed_four = 0
    open_four = 0

    five = 0
    
    if total_consec == 1:
        if close_threat:
            closed_two += 1
        if semi_close:
            semi_closed_two += 1
        if open_threat:
            open_two += 1
    if total_consec == 2:
        if close_threat:
            closed_three += 1
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
    if total_consec == 3:
        if close_threat:
            closed_four += 1
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
    if total_consec >= 4:
        five += 1
    
    has_empty = False
    if r_additional and l_consec + r_additional == 2:
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
        has_empty = True
    if l_additional and r_consec + l_additional == 2:
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
        has_empty = True
    if r_additional and l_consec + r_additional == 3:
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
        has_empty = True
    if l_additional and r_consec + l_additional == 3:
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
        has_empty = True

    #Check vulnerability
    open_get_eat = 0
    if l_starting_op and r_could_get_eat:
        open_get_eat += 1
    if r_starting_op and l_could_get_eat:
        open_get_eat += 1

    # print("closed_two:") 
    # print(closed_two)
    # print("semi_close_two:")
    # print(semi_closed_two)
    # print("open_two:")
    # print(open_two)
    # print("closed_three:")
    # print(closed_three)
    # print("semi_closed_three")
    # print(semi_closed_three)
    # print("open_three")
    # print(open_three)
    # print("closed_four")
    # print(closed_four)
    # print("semi_close_four")
    # print(semi_closed_four)
    # print("open_four")
    # print(open_four)
    # print("five")
    # print(five)
    
    return has_empty, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five, open_get_eat


@njit("UniTuple(int64[:], 2)(int64[:,:], int64, int64)", fastmath=True)
def get_diags(board, row_index, col_index):
    lr_diags = np.diag(board, col_index - row_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    return lr_diags, rl_diags

@njit
def get_score(has_empty, is_enemy, player_eat, enemy_eat, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five, open_get_eat):
    # Player series
    minus_empty = 0
    if has_empty:
        minus_empty = 100

    if not is_enemy:
        if five:
            return multiplicator_five - minus_empty
        elif open_four:
            return multiplicator_open_four - minus_empty
        elif semi_closed_four:
            return multiplicator_semi_closed_four - minus_empty
        elif open_three:
            return multiplicator_open_three - minus_empty
        elif semi_closed_three:
            return multiplicator_semi_closed_three - minus_empty
        elif open_two:
            return multiplicator_open_two
        elif semi_closed_two:
            return multiplicator_semi_close_two - minus_empty
        return 0
    else:
        if five:
            return multiplicator_enemy_five - minus_empty
        elif open_four:
            return multiplicator_enemy_open_four - minus_empty
        elif semi_closed_four:
            return multiplicator_enemy_semi_closed_four - minus_empty
        elif open_three:
            return multiplicator_enemy_open_three - minus_empty
        elif semi_closed_three:
            return multiplicator_enemy_semi_closed_three - minus_empty
        elif open_two:
            return multiplicator_enemy_open_two - minus_empty
        elif semi_closed_two:
            return multiplicator_enemy_semi_close_two - minus_empty
        return 0

@njit
# @njit("Tuple((int64, List(int64[:])))(int64[:,:], int64[:], boolean, int64, int64, int64)", fastmath=True)
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position

    lr_diags, rl_diags = get_diags(board, row_index, col_index)
    rows = board[row_index, :]
    columns = board[:, col_index]
    
    captured_stones = []

    # print(lr_diags)
    lr_starting_index = col_index if row_index > col_index else row_index
    has_empty_lr, capture_left_lr, capture_right_lr, closed_two_lr, semi_closed_two_lr, open_two_lr, closed_three_lr, semi_closed_three_lr, open_three_lr, closed_four_lr, semi_closed_four_lr, open_four_lr, five_lr, open_get_eat_lr = check_line(lr_diags, lr_starting_index, player)
    result_lr = get_score(has_empty_lr, False, player_eat, enemy_eat, capture_left_lr, capture_right_lr, closed_two_lr, semi_closed_two_lr, open_two_lr, closed_three_lr, semi_closed_three_lr, open_three_lr, closed_four_lr, semi_closed_four_lr, open_four_lr, five_lr, open_get_eat_lr)
    # print(rl_diags)
    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
    has_empty_rl, capture_left_rl, capture_right_rl, closed_two_rl, semi_closed_two_rl, open_two_rl, closed_three_rl, semi_closed_three_rl, open_three_rl, closed_four_rl, semi_closed_four_rl, open_four_rl, five_rl, open_get_eat_rl = check_line(rl_diags, rl_starting_index, player)
    result_rl = get_score(has_empty_rl, False, player_eat, enemy_eat, capture_left_rl, capture_right_rl, closed_two_rl, semi_closed_two_rl, open_two_rl, closed_three_rl, semi_closed_three_rl, open_three_rl, closed_four_rl, semi_closed_four_rl, open_four_rl, five_rl, open_get_eat_rl)
    # print(rows)
    has_empty_row, capture_left_row, capture_right_row, closed_two_row, semi_closed_two_row, open_two_row, closed_three_row, semi_closed_three_row, open_three_row, closed_four_row, semi_closed_four_row, open_four_row, five_row, open_get_eat_row = check_line(rows, col_index, player)
    result_row = get_score(has_empty_row, False, player_eat, enemy_eat, capture_left_row, capture_right_row, closed_two_row, semi_closed_two_row, open_two_row, closed_three_row, semi_closed_three_row, open_three_row, closed_four_row, semi_closed_four_row, open_four_row, five_row, open_get_eat_row)
    # print(columns)
    has_empty_col, capture_left_col, capture_right_col, closed_two_col, semi_closed_two_col, open_two_col, closed_three_col, semi_closed_three_col, open_three_col, closed_four_col, semi_closed_four_col, open_four_col, five_col, open_get_eat_col = check_line(columns, row_index, player)
    result_col = get_score(has_empty_col, False, player_eat, enemy_eat, capture_left_col, capture_right_col, closed_two_col, semi_closed_two_col, open_two_col, closed_three_col, semi_closed_three_col, open_three_col, closed_four_col, semi_closed_four_col, open_four_col, five_col, open_get_eat_col)

    # print(f"closed_two: {closed_two_lr + closed_two_rl + closed_two_row + closed_two_col}") 
    # # print(closed_two_lr + closed_two_rl + closed_two_row + closed_two_col)
    # print(f"semi_close_two: {semi_closed_two_lr + semi_closed_two_rl + semi_closed_two_row + semi_closed_two_col}")
    # print(f"open_two: {open_two_lr + open_two_rl + open_two_row + open_two_col}")
    # print(f"closed_three: {closed_three_lr + closed_three_rl + closed_three_row + closed_three_col}")
    # print(f"semi_closed_three: {semi_closed_three_lr + semi_closed_three_rl + semi_closed_three_row + semi_closed_three_col}")
    # print(f"open_three: {open_three_lr + open_three_rl + open_three_row + open_three_col}")
    # print(f"closed_four: {closed_four_lr + closed_four_rl + closed_four_row + closed_four_col}")
    # print(f"semi_close_four: {semi_closed_four_lr + semi_closed_four_rl + semi_closed_four_row + semi_closed_four_col}")
    # print(f"open_four: {open_four_lr + open_four_rl + open_four_row + open_four_col}")
    # print(f"five: {five_lr + five_rl + five_row + five_col}")

    # score = max(result_lr, result_rl, result_row, result_col)

    op_has_empty_lr, op_capture_left_lr, op_capture_right_lr, op_closed_two_lr, op_semi_closed_two_lr, op_open_two_lr, op_closed_three_lr, op_semi_closed_three_lr, op_open_three_lr, op_closed_four_lr, op_semi_closed_four_lr, op_open_four_lr, op_five_lr, op_open_get_eat_lr = check_line(lr_diags, lr_starting_index, player * -1)
    op_result_lr = get_score(op_has_empty_lr, True, enemy_eat, player_eat, op_capture_left_lr, op_capture_right_lr, op_closed_two_lr, op_semi_closed_two_lr, op_open_two_lr, op_closed_three_lr, op_semi_closed_three_lr, op_open_three_lr, op_closed_four_lr, op_semi_closed_four_lr, op_open_four_lr, op_five_lr, op_open_get_eat_lr)
    op_has_empty_rl, op_capture_left_rl, op_capture_right_rl, op_closed_two_rl, op_semi_closed_two_rl, op_open_two_rl, op_closed_three_rl, op_semi_closed_three_rl, op_open_three_rl, op_closed_four_rl, op_semi_closed_four_rl, op_open_four_rl, op_five_rl, op_open_get_eat_rl = check_line(rl_diags, rl_starting_index, player * -1)
    op_result_rl = get_score(op_has_empty_rl, True, enemy_eat, player_eat, op_capture_left_rl, op_capture_right_rl, op_closed_two_rl, op_semi_closed_two_rl, op_open_two_rl, op_closed_three_rl, op_semi_closed_three_rl, op_open_three_rl, op_closed_four_rl, op_semi_closed_four_rl, op_open_four_rl, op_five_rl, op_open_get_eat_rl)
    op_has_empty_row, op_capture_left_row, op_capture_right_row, op_closed_two_row, op_semi_closed_two_row, op_open_two_row, op_closed_three_row, op_semi_closed_three_row, op_open_three_row, op_closed_four_row, op_semi_closed_four_row, op_open_four_row, op_five_row, op_open_get_eat_row = check_line(rows, col_index, player * -1)
    op_result_row = get_score(op_has_empty_row, True, enemy_eat, player_eat, op_capture_left_row, op_capture_right_row, op_closed_two_row, op_semi_closed_two_row, op_open_two_row, op_closed_three_row, op_semi_closed_three_row, op_open_three_row, op_closed_four_row, op_semi_closed_four_row, op_open_four_row, op_five_row, op_open_get_eat_row)
    op_has_empty_col, op_capture_left_col, op_capture_right_col, op_closed_two_col, op_semi_closed_two_col, op_open_two_col, op_closed_three_col, op_semi_closed_three_col, op_open_three_col, op_closed_four_col, op_semi_closed_four_col, op_open_four_col, op_five_col, op_open_get_eat_col = check_line(columns, row_index, player * -1)
    op_result_col = get_score(op_has_empty_col, True, enemy_eat, player_eat, op_capture_left_col, op_capture_right_col, op_closed_two_col, op_semi_closed_two_col, op_open_two_col, op_closed_three_col, op_semi_closed_three_col, op_open_three_col, op_closed_four_col, op_semi_closed_four_col, op_open_four_col, op_five_col, op_open_get_eat_col)

    # print(f"op_closed_two: {op_closed_two_lr + op_closed_two_rl + op_closed_two_row + op_closed_two_col}")
    # print(f"op_semi_close_two: {op_semi_closed_two_lr + op_semi_closed_two_rl + op_semi_closed_two_row + op_semi_closed_two_col}")
    # print(f"op_open_two: {op_open_two_lr + op_open_two_rl + op_open_two_row + op_open_two_col}")
    # print(f"op_closed_three: {op_closed_three_lr + op_closed_three_rl + op_closed_three_row + op_closed_three_col}")
    # print(f"op_semi_closed_three: {op_semi_closed_three_lr + op_semi_closed_three_rl + op_semi_closed_three_row + op_semi_closed_three_col}")
    # print(f"op_open_three: {open_three_lr + op_open_three_rl + op_open_three_row + op_open_three_col}")
    # print(f"op_closed_four: {op_closed_four_lr + op_closed_four_rl + op_closed_four_row + op_closed_four_col}")
    # print(f"op_semi_close_four: {op_semi_closed_four_lr + op_semi_closed_four_rl + op_semi_closed_four_row + op_semi_closed_four_col}")
    # print(f"op_open_four: {op_open_four_lr + op_open_four_rl + op_open_four_row + op_open_four_col}")
    # print(f"op_five: {op_five_lr + op_five_rl + op_five_row + op_five_col}")

    score = max(result_lr, result_rl, result_row, result_col, op_result_lr, op_result_rl, op_result_row, op_result_col)

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

    if eat_move:
        adding_eat = eat_value(eat_move + player_eat) #/ 10

    open_get_eat = open_get_eat_lr + open_get_eat_rl + open_get_eat_row + open_get_eat_col
    minus_vulnerability = 0
    if open_get_eat:
        minus_vulnerability = eat_value(eat_move + enemy_eat)

    score = score + adding_eat - minus_vulnerability
    # print("Score:")
    # print(score)

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

    if not maximizing_player:
        score *= -1

    return score / depth, captured_stones
    # return score, captured_stones, is_win, line_axis
