import board_utils
import numpy as np

from numba import njit, int64
from check_breakable import check_if_breakable

multiplicator_five = 11_000
multiplicator_open_four = 1_490
multiplicator_open_three = 450
multiplicator_semi_closed_four = 50
multiplicator_semi_closed_three = 39
multiplicator_open_two = 1
multiplicator_semi_close_two = 0

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


@njit("Tuple((int64, int64, boolean, boolean))(int64[:], int64, boolean)", fastmath=True)
def check_side(side, player, eating=False):
    consec = 0
    additional = 0
    is_after_blank = False
    is_consec = True
    block = False

    #If is on the board side
    if len(side) == 0:
        return 0, 0, False, True
    
    #Only if eating
    if len(side) >= 3:
        if side[0] == -player and side[1] == -player and side[2] == player:
            new_side = np.copy(side)
            new_side[0] = 0
            new_side[1] = 0
            return check_side(new_side, player, eating=True)

    for i in range(0, min(len(side), 6)):
        if side[i] == player:
            if is_consec:
                consec += 1
            else:
                additional += 1
        elif side[i] == 0:
            if is_after_blank:
                return consec, additional, eating, block
            is_after_blank = True
            is_consec = False
        elif side[i] == -player:
            if is_after_blank:
                if not additional:
                    return consec, additional, eating, False
            return consec, additional, eating, True
    if i == 0 and side[i] == 0:
        return consec, additional, eating, block
    if i == len(side) - 1:
        if not(is_after_blank and not additional):
            block = True
    return consec, additional, eating, block


@njit("Tuple((boolean, boolean, boolean, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64))(int64[:], int64, int64)", fastmath=True)
def check_line(line, starting_index, player):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    
    l_consec, l_additional, l_eating, l_block = check_side(left, player, False)
    r_consec, r_additional, r_eating, r_block = check_side(right, player, False)
    
    
    close_threat = False
    semi_closed = False
    open_threat = False
    
    if l_block and r_block:
        close_threat = True
    elif (l_block and not r_block) or (not l_block and r_block):
        semi_closed = True
    else:
        if (l_consec or r_consec) or (not r_consec and not r_additional and l_additional) or (not l_consec and not l_additional and r_additional):
            open_threat = True

    total_stone = l_consec + l_additional + r_consec + r_additional
    has_empty = True if (l_additional or r_additional) else False
        
    # Player serie
    five = 0
    open_four = 0
    semi_closed_four = 0
    closed_four = 0
    open_three = 0
    semi_closed_three = 0
    closed_three = 0
    open_two = 0
    semi_closed_two = 0
    closed_two = 0
    
    if total_stone >= 4:
        five += 1
    elif total_stone == 3:
        if close_threat:
            closed_four += 1
        if semi_closed:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
    elif total_stone == 2:
        if close_threat:
            closed_three += 1
        if semi_closed:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
    elif total_stone == 1:
        if close_threat:
            closed_two += 1
        if semi_closed:
            semi_closed_two += 1
        if open_threat:
            open_two += 1

    return has_empty, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five


@njit("boolean(boolean, int64)", fastmath=True)
def five_and_enemy_capture(five, enemy_total_eat):
    if five and enemy_total_eat == 4:
        return True
    return False


@njit
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position
    lr_diags, rl_diags, row, column = board_utils.get_vectors(board, row_index, col_index)
    
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

    score = result_lr + result_rl + result_row + result_col
    # score = max(result_lr, result_rl, result_row, result_col)

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