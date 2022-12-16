import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_

multiplicator_five = 11_000
multiplicator_open_four = 1_490
multiplicator_open_three = 1_450
multiplicator_semi_closed_four = 500
multiplicator_semi_closed_three = 390
multiplicator_open_two = 1
multiplicator_semi_close_two = 0

@njit("(int64)(int64)", fastmath=True)
def eat_value(eat_number):
    if eat_number >= 5:
        return 100_000
    if eat_number == 4:
        return 1_400
    if eat_number == 3:
        return 1_100
    if eat_number == 2:
        return 1_050
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


@njit("Tuple((boolean, boolean, boolean, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64))(int64[:], int64, int64)", fastmath=True)
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

    return has_empty, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five


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

@njit("(int64)(boolean, int64, int64, int64, int64, int64, int64, int64)", fastmath=True)
def get_score(has_empty, semi_closed_two, open_two, semi_closed_three, open_three, semi_closed_four, open_four, five):
    # Player series
    minus_empty = 0
    if has_empty:
        minus_empty = 100

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
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position
    lr_diags, rl_diags, row, column = get_vectors(board, row_index, col_index)
    
    captured_stones = []

    defend_breaking_five = 0

    lr_starting_index = col_index if row_index > col_index else row_index
    has_empty_lr, capture_left_lr, capture_right_lr, closed_two_lr, semi_closed_two_lr, open_two_lr, closed_three_lr, semi_closed_three_lr, open_three_lr, closed_four_lr, semi_closed_four_lr, open_four_lr, five_lr = check_line(lr_diags, lr_starting_index, player)
    if five_and_enemy_capture(five_lr, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(0), lr_diags, lr_starting_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = 10_000
    result_lr = get_score(has_empty_lr, semi_closed_two_lr, open_two_lr, semi_closed_three_lr, open_three_lr, semi_closed_four_lr, open_four_lr, five_lr)

    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
    has_empty_rl, capture_left_rl, capture_right_rl, closed_two_rl, semi_closed_two_rl, open_two_rl, closed_three_rl, semi_closed_three_rl, open_three_rl, closed_four_rl, semi_closed_four_rl, open_four_rl, five_rl = check_line(rl_diags, rl_starting_index, player)
    if five_and_enemy_capture(five_rl, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(1), rl_diags, rl_starting_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = 10_000
    result_rl = get_score(has_empty_rl, semi_closed_two_rl, open_two_rl, semi_closed_three_rl, open_three_rl, semi_closed_four_rl, open_four_rl, five_rl)

    has_empty_row, capture_left_row, capture_right_row, closed_two_row, semi_closed_two_row, open_two_row, closed_three_row, semi_closed_three_row, open_three_row, closed_four_row, semi_closed_four_row, open_four_row, five_row = check_line(row, col_index, player)
    if five_and_enemy_capture(five_row, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(2), row, col_index, player, row_index,col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = 10_000
    result_row = get_score(has_empty_row, semi_closed_two_row, open_two_row, semi_closed_three_row, open_three_row, semi_closed_four_row, open_four_row, five_row)

    has_empty_col, capture_left_col,capture_right_col, closed_two_col, semi_closed_two_col, open_two_col, closed_three_col, semi_closed_three_col, open_three_col, closed_four_col, semi_closed_four_col, open_four_col, five_col = check_line(column, row_index, player)
    if five_and_enemy_capture(five_col, enemy_eat):
        is_breakable, break_pos = check_if_breakable(board, int64(3), column, row_index, player, row_index, col_index)
        if is_breakable:
            position = break_pos
            defend_breaking_five = 10_000
    result_col = get_score(has_empty_col, semi_closed_two_col, open_two_col, semi_closed_three_col, open_three_col, semi_closed_four_col, open_four_col, five_col)

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

    if eat_move:
        adding_eat = eat_value(eat_move + player_eat) #/ 10

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


    is_win = True if score >= 10_000 else False
    is_forbidden = True if open_three_lr + open_three_rl + open_three_row + open_three_col >= 2 else False

    if not maximizing_player:
        score *= -1

    return position, score / depth, captured_stones, is_win, is_forbidden, eat_move