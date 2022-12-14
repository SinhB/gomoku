import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_


multiplicator_five = 500_000_000
multiplicator_enemy_five = 45_000_000
multiplicator_enemy_open_four = 25_000_000
multiplicator_enemy_semi_closed_four = 20_000_000
multiplicator_enemy_open_three = 1_000_000
multiplicator_open_four = 1_500_000
multiplicator_open_three = 100_000
multiplicator_semi_closed_four = 20_000
multiplicator_enemy_semi_closed_three = 10_000
multiplicator_semi_closed_three = 5_000
multiplicator_open_two = 50
multiplicator_semi_close_two = 5
multiplicator_enemy_semi_close_two = 10
multiplicator_enemy_open_two = 100

# # Player series multiplicator
# multiplicator_closed_two = 10
# multiplicator_semi_close_two = 50
# multiplicator_open_two = 500

# multiplicator_closed_three = 20
# multiplicator_semi_closed_three = 1_000
# multiplicator_open_three = 10_000

# multiplicator_closed_four = 40
# multiplicator_semi_closed_four = 20_000
# multiplicator_open_four = 100_000

# multiplicator_five = 100_000_000

# # Block enemy series multiplicator
# multiplicator_enemy_closed_two = 20
# multiplicator_enemy_semi_close_two = 100
# multiplicator_enemy_open_two = 1000

# multiplicator_enemy_closed_three = 40
# multiplicator_enemy_semi_closed_three = 2_000
# multiplicator_enemy_open_three = 400_000

# multiplicator_enemy_closed_four = 80
# multiplicator_enemy_semi_closed_four = 1_000_000
# multiplicator_enemy_open_four = 5_000_000

# multiplicator_enemy_five = 50_000_000

# Eating move
multiplicator_open_eat_move = 200

# @njit("Tuple((int64, int64, boolean, boolean, boolean, int64))(int64[:], int64)", fastmath=True)
# def check_side(side, player):
#     # Number of consecutive stone placed directly next to the one played
#     consecutive = 0
#     # Number of enemy consecutive stone placed directly next to the one played
#     consecutive_enemy = 0
#     # Number of consecutive stone separated by one zero from the consecutive ones
#     additional = 0
#     # Is there an empty space at the end of the last serie of stone
#     empty_space = False
#     # Eating enemy
#     eating_enemy = False
#     # Open eating move
#     open_eating_move = False

#     is_consecutive = True
#     check_eating_enemy = True
#     check_open_eating_move = True
#     is_after_one_zero = False

#     for i in range(0, min(len(side), 6)):
#         if is_consecutive:
#             if side[i] == player:
#                 consecutive += 1
#             else:
#                 is_consecutive = False

#         if check_eating_enemy or check_open_eating_move and not is_after_one_zero:
#             if side[i] == player and consecutive_enemy == 2:
#                 # Return eating_move
#                 return 0, 0, False, True, False, consecutive_enemy
#             elif side[i] == 0 and consecutive_enemy == 2:
#                 # Return open_eating_move
#                 return 0, 0, True, False, True, consecutive_enemy
#             elif side[i] == player * -1:
#                 consecutive_enemy += 1
#             else:
#                 check_eating_enemy = False
#                 check_open_eating_move = False

#         if side[i] == 0:
#             if i == 0 or consecutive > 0 or consecutive_enemy > 0:
#                 empty_space = True
#             if is_after_one_zero:
#                 break
#             else:
#                 is_after_one_zero = True
#             check_eating_enemy = False
#             # check_open_eating_move = False
        
#         if is_after_one_zero:
#             if side[i] == player:
#                 additional += 1
#             # else:
#             #     break
        
#     return consecutive, additional, empty_space, eating_enemy, open_eating_move, consecutive_enemy

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


@njit("Tuple((int64, boolean, boolean, int64, int64, int64, int64, int64, int64, int64, int64, int64, int64))(int64[:], int64, int64, int64, int64)", fastmath=True)
def check_line(line, starting_index, player, player_eat, enemy_eat):
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
            
    if r_additional and l_consec + r_additional == 2:
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
    if l_additional and r_consec + l_additional == 2:
        if semi_close:
            semi_closed_three += 1
        if open_threat:
            open_three += 1
        
    if r_additional and l_consec + r_additional == 3:
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1
    if l_additional and r_consec + l_additional == 3:
        if semi_close:
            semi_closed_four += 1
        if open_threat:
            open_four += 1

    #Check vulnerability
    open_get_eat = 0
    if l_starting_op and r_could_get_eat:
        open_get_eat += 1
    if r_starting_op and l_could_get_eat:
        open_get_eat += 1

    score = 1
    # Player series
    score += semi_closed_two * multiplicator_semi_close_two
    score += open_two * multiplicator_open_two

    score += semi_closed_three * multiplicator_semi_closed_three
    score += open_three * multiplicator_open_three

    score += semi_closed_four * multiplicator_semi_closed_four
    score += open_four * multiplicator_open_four

    score += five * multiplicator_five

    eat_move = l_eating + r_eating

    if eat_move:
        score += ((eat_move + player_eat + 1) ** 10) * 10

    # if open_get_eat:
    #     score += (open_get_eat + enemy_eat + 1) ** 7

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
    
    return score, l_eating, r_eating, closed_two, semi_closed_two, open_two, closed_three, semi_closed_three, open_three, closed_four, semi_closed_four, open_four, five

# @functools.cache
# @njit("UniTuple(int64, 23)(int64[:], int64, int64)", fastmath=True)
# @njit("Tuple((int64, boolean, boolean))(int64[:], int64, int64, int64, int64)", fastmath=True)
# def check_line(line, starting_index, player, player_eat, enemy_eat):
#     left = line[0:starting_index][::-1]
#     right = line[starting_index+1:]

#     l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_consecutive_enemy = check_side(left, player)
#     r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_consecutive_enemy = check_side(right, player)

#     total_consecutive = l_consecutive + r_consecutive
#     total_consecutive_enemy = l_consecutive_enemy + r_consecutive_enemy
#     total_empty_space = l_empty_space + r_empty_space
#     # print(f"? = {total_consecutive_enemy}")

#     eat_move = l_eating_enemy + r_eating_enemy
#     open_eat_move = l_open_eating_move + r_open_eating_move
#     open_get_eat_move = 0
#     if l_consecutive == 2 and l_empty_space == False:
#         open_get_eat_move += 1
#     if r_consecutive == 2 and r_empty_space == False:
#         open_get_eat_move += 1

#     # Player serie
#     closed_two = 0
#     semi_close_two = 0
#     open_two = 0

#     closed_three = 0
#     semi_closed_three = 0
#     open_three = 0

#     closed_four = 0
#     semi_closed_four = 0
#     open_four = 0

#     five = 0

#     if l_consecutive + l_additional == 3:
#         open_three += 1
#     if r_consecutive + r_additional == 3:
#         open_three += 1

#     if total_consecutive == 1:
#         if total_empty_space == 2:
#             open_two += 1
#         elif total_empty_space == 1:
#             semi_close_two += 1
#         else:
#             closed_two += 1

#     elif total_consecutive == 2:
#         if total_empty_space == 2:
#             open_three += 1
#         elif total_empty_space == 1:
#             semi_closed_three += 1
#         else:
#             closed_three += 1

#     elif total_consecutive == 3:
#         if total_empty_space == 2:
#             open_four += 1
#         elif total_empty_space == 1:
#             semi_closed_four += 1
#         else:
#             closed_four += 1

#     elif total_consecutive >= 4:
#         five += 1
    
#     # Enemy player serie
#     enemy_closed_two = 0
#     enemy_semi_close_two = 0
#     enemy_open_two = 0

#     enemy_closed_three = 0
#     enemy_semi_closed_three = 0
#     enemy_open_three = 0

#     enemy_closed_four = 0
#     enemy_semi_closed_four = 0
#     enemy_open_four = 0

#     enemy_five = 0

#     if total_consecutive_enemy == 1:
#         if total_empty_space == 2:
#             enemy_open_two += 1
#         elif total_empty_space == 1:
#             enemy_semi_close_two += 1
#         else:
#             enemy_closed_two += 1

#     elif total_consecutive_enemy == 2:
#         if total_empty_space == 1:
#             enemy_open_three += 1
#         elif total_empty_space == 0:
#             enemy_semi_closed_three += 1
#         else:
#             enemy_closed_three += 1

#     elif total_consecutive_enemy == 3:
#         if total_empty_space == 2:
#             enemy_open_four += 1
#         elif total_empty_space == 1:
#             enemy_semi_closed_four += 1
#         else:
#             enemy_closed_four += 1

#     elif total_consecutive_enemy >= 4:
#         enemy_five += 1

#     score = 1
#     # Player series
#     score += semi_close_two * multiplicator_semi_close_two
#     score += open_two * multiplicator_open_two

#     score += semi_closed_three * multiplicator_semi_closed_three
#     score += open_three * multiplicator_open_three

#     score += semi_closed_four * multiplicator_semi_closed_four
#     score += open_four * multiplicator_open_four

#     score += five * multiplicator_five

#     # Enemy series
#     score += enemy_semi_close_two * multiplicator_enemy_semi_close_two
#     score += enemy_open_two * multiplicator_enemy_open_two

#     score += enemy_semi_closed_three * multiplicator_enemy_semi_closed_three
#     score += enemy_open_three * multiplicator_enemy_open_three

#     score += enemy_semi_closed_four * multiplicator_enemy_semi_closed_four
#     score += enemy_open_four * multiplicator_enemy_open_four

#     score += enemy_five * multiplicator_enemy_five

#     if eat_move:
#         score += ((eat_move + player_eat + 1) ** 10) * 10

#     if open_eat_move:
#         score += (open_eat_move + player_eat + 1) ** 7

#     if open_get_eat_move:
#         score += (open_get_eat_move + enemy_eat + 1) ** 7

#     return score, l_eating_enemy, r_eating_enemy


@njit("UniTuple(int64[:], 2)(int64[:,:], int64, int64)", fastmath=True)
def get_diags(board, row_index, col_index):
    lr_diags = np.diag(board, col_index - row_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    return lr_diags, rl_diags

@njit
# @njit("Tuple((int64, List(int64[:])))(int64[:,:], int64[:], boolean, int64, int64, int64)", fastmath=True)
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    # if not maximizing_player:
    #     player = player * -1

    row_index, col_index = position

    lr_diags, rl_diags = get_diags(board, row_index, col_index)
    rows = board[row_index, :]
    columns = board[:, col_index]
    
    captured_stones = []

    # print("PLAYER")
    # print(player)
    print("POSITION:")
    print(position)


    print(lr_diags)
    result_lr, capture_left_lr, capture_right_lr, closed_two_lr, semi_closed_two_lr, open_two_lr, closed_three_lr, semi_closed_three_lr, open_three_lr, closed_four_lr, semi_closed_four_lr, open_four_lr, five_lr = check_line(lr_diags, row_index, player, player_eat, enemy_eat)
    print(rl_diags)
    result_rl, capture_left_rl, capture_right_rl, closed_two_rl, semi_closed_two_rl, open_two_rl, closed_three_rl, semi_closed_three_rl, open_three_rl, closed_four_rl, semi_closed_four_rl, open_four_rl, five_rl = check_line(rl_diags, row_index, player, player_eat, enemy_eat)
    print(rows)
    result_row, capture_left_row, capture_right_row, closed_two_row, semi_closed_two_row, open_two_row, closed_three_row, semi_closed_three_row, open_three_row, closed_four_row, semi_closed_four_row, open_four_row, five_row = check_line(rows, col_index, player, player_eat, enemy_eat)
    print(columns)
    result_col, capture_left_col, capture_right_col, closed_two_col, semi_closed_two_col, open_two_col, closed_three_col, semi_closed_three_col, open_three_col, closed_four_col, semi_closed_four_col, open_four_col, five_col = check_line(columns, row_index, player, player_eat, enemy_eat)

    print("closed_two:") 
    print(closed_two_lr + closed_two_rl + closed_two_row + closed_two_col)
    print("semi_close_two:")
    print(semi_closed_two_lr + semi_closed_two_rl + semi_closed_two_row + semi_closed_two_col)
    print("open_two:")
    print(open_two_lr + open_two_rl + open_two_row + open_two_col)
    print("closed_three:")
    print(closed_three_lr + closed_three_rl + closed_three_row + closed_three_col)
    print("semi_closed_three")
    print(semi_closed_three_lr + semi_closed_three_rl + semi_closed_three_row + semi_closed_three_col)
    print("open_three")
    print(open_three_lr + open_three_rl + open_three_row + open_three_col)
    print("closed_four")
    print(closed_four_lr + closed_four_rl + closed_four_row + closed_four_col)
    print("semi_close_four")
    print(semi_closed_four_lr + semi_closed_four_rl + semi_closed_four_row + semi_closed_four_col)
    print("open_four")
    print(open_four_lr + open_four_rl + open_four_row + open_four_col)
    print("five")
    print(five_lr + five_lr + five_row + five_col)

    score = result_lr + result_rl + result_row + result_col

    op_result_lr, _, _, _, _, _, _, _, _, _, _, _, _ = check_line(lr_diags, row_index, player * -1, enemy_eat, player_eat)
    op_result_rl, _, _, _, _, _, _, _, _, _, _, _, _ = check_line(rl_diags, row_index, player * -1, enemy_eat, player_eat)
    op_result_row, _, _, _, _, _, _, _, _, _, _, _, _ = check_line(rows, col_index, player * -1, enemy_eat, player_eat)
    op_result_col, _, _, _, _, _, _, _, _, _, _, _, _ = check_line(columns, row_index, player * -1, enemy_eat, player_eat)

    score += op_result_lr + op_result_rl + op_result_row + op_result_col

    
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
