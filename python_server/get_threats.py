import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_

@njit("(int64)(int64)", fastmath=True)
def eat_value(eat_number):
    if eat_number == 0:
        return 9
    elif eat_number == 1:
        return 100_000 
    elif eat_number == 2:
        return 500_000
    elif eat_number == 3:
        return 1_000_000
    elif eat_number == 4:
        return 10_000_000
    return 100_000_000

multiplicator_five = 500_000_000
multiplicator_enemy_five = 250_000_000
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

@njit("Tuple((int64, int64, boolean, boolean, boolean, int64))(int64[:], int64)", fastmath=True)
def check_side(side, player):
    # Number of consecutive stone placed directly next to the one played
    consecutive = 0
    # Number of enemy consecutive stone placed directly next to the one played
    consecutive_enemy = 0
    # Number of consecutive stone separated by one zero from the consecutive ones
    additional = 0
    # Is there an empty space at the end of the last serie of stone
    empty_space = False
    # Eating enemy
    eating_enemy = False
    # Open eating move
    open_eating_move = False

    is_consecutive = True
    check_eating_enemy = True
    check_open_eating_move = True
    is_after_one_zero = False

    for i in range(0, min(len(side), 6)):
        if is_consecutive:
            if side[i] == player:
                consecutive += 1
            else:
                is_consecutive = False

        if (check_eating_enemy or check_open_eating_move) and not is_after_one_zero:
            if side[i] == player and consecutive_enemy == 2:
                # Return eating_move
                return 0, 0, True, True, False, consecutive_enemy
            elif side[i] == 0 and consecutive_enemy == 2:
                # Return open_eating_move
                return 0, 0, True, False, True, consecutive_enemy
            elif side[i] == player * -1:
                consecutive_enemy += 1
            else:
                check_eating_enemy = False
                check_open_eating_move = False

        if side[i] == 0:
            if i == 0 or consecutive > 0 or consecutive_enemy > 0:
                if not (consecutive == 0 and consecutive_enemy == 0):
                    empty_space = True
            if is_after_one_zero:
                break
            else:
                is_after_one_zero = True
            check_eating_enemy = False
            # check_open_eating_move = False
        
        if is_after_one_zero:
            if side[i] == player:
                additional += 1
            # else:
            #     break
        
    return consecutive, additional, empty_space, eating_enemy, open_eating_move, consecutive_enemy

# @functools.cache
# @njit("UniTuple(int64, 23)(int64[:], int64, int64)", fastmath=True)
@njit("Tuple((int64, boolean, boolean))(int64[:], int64, int64, int64, int64)", fastmath=True)
def check_line(line, starting_index, player, player_eat, enemy_eat):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]

    print(line)
    print(left)
    print(right)

    l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_consecutive_enemy = check_side(left, player)
    print(l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_consecutive_enemy)
    r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_consecutive_enemy = check_side(right, player)
    print(r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_consecutive_enemy)
    print("\n\n")

    total_consecutive = l_consecutive + r_consecutive + 1
    total_consecutive_enemy = l_consecutive_enemy + r_consecutive_enemy
    total_empty_space = l_empty_space + r_empty_space

    eat_move = l_eating_enemy + r_eating_enemy
    open_eat_move = l_open_eating_move + r_open_eating_move
    open_get_eat_move = 0
    if l_consecutive == 2 and l_empty_space == False:
        open_get_eat_move += 1
    if r_consecutive == 2 and r_empty_space == False:
        open_get_eat_move += 1

    # Player serie
    closed_two = 0
    semi_close_two = 0
    open_two = 0

    closed_three = 0
    semi_closed_three = 0
    open_three = 0

    closed_four = 0
    semi_closed_four = 0
    open_four = 0

    five = 0

    if l_consecutive + l_additional == 2 and ((r_eating_enemy or r_empty_space) or l_empty_space):
        open_three += 1
    if r_consecutive + r_additional == 2 and ((l_eating_enemy or l_empty_space) or r_empty_space):
        open_three += 1

    if total_consecutive == 1:
        if total_empty_space == 2:
            open_two += 1
        elif total_empty_space == 1:
            semi_close_two += 1
        else:
            closed_two += 1

    elif total_consecutive == 2:
        if total_empty_space == 2:
            open_three += 1
        elif total_empty_space == 1:
            semi_closed_three += 1
        else:
            closed_three += 1

    elif total_consecutive == 3:
        if total_empty_space == 2:
            open_four += 1
        elif total_empty_space == 1:
            semi_closed_four += 1
        else:
            closed_four += 1

    elif total_consecutive >= 4:
        five += 1
    
    # Enemy player serie
    enemy_closed_two = 0
    enemy_semi_close_two = 0
    enemy_open_two = 0

    enemy_closed_three = 0
    enemy_semi_closed_three = 0
    enemy_open_three = 0

    enemy_closed_four = 0
    enemy_semi_closed_four = 0
    enemy_open_four = 0

    enemy_five = 0

    if total_consecutive_enemy == 1:
        if total_empty_space == 2:
            enemy_open_two += 1
        elif total_empty_space == 1:
            enemy_semi_close_two += 1
        else:
            enemy_closed_two += 1

    elif total_consecutive_enemy == 2:
        if total_empty_space == 1:
            enemy_open_three += 1
        elif total_empty_space == 0:
            enemy_semi_closed_three += 1
        else:
            enemy_closed_three += 1

    elif total_consecutive_enemy == 3:
        if total_empty_space == 2:
            enemy_open_four += 1
        elif total_empty_space == 1:
            enemy_semi_closed_four += 1
        else:
            enemy_closed_four += 1

    elif total_consecutive_enemy >= 4:
        enemy_five += 1

    score = 1
    # Player series
    score += semi_close_two * multiplicator_semi_close_two
    score += open_two * multiplicator_open_two

    score += semi_closed_three * multiplicator_semi_closed_three
    score += open_three * multiplicator_open_three

    score += semi_closed_four * multiplicator_semi_closed_four
    score += open_four * multiplicator_open_four

    score += five * multiplicator_five

    # Enemy series
    score += enemy_semi_close_two * multiplicator_enemy_semi_close_two
    score += enemy_open_two * multiplicator_enemy_open_two

    score += enemy_semi_closed_three * multiplicator_enemy_semi_closed_three
    score += enemy_open_three * multiplicator_enemy_open_three

    score += enemy_semi_closed_four * multiplicator_enemy_semi_closed_four
    score += enemy_open_four * multiplicator_enemy_open_four

    score += enemy_five * multiplicator_enemy_five

    if eat_move:
        score += eat_value(eat_move + player_eat + 1)
        # score += 100_000 + ((eat_move + player_eat + 1) ** 10)

    if open_eat_move:
        score += eat_value(open_eat_move + player_eat) / 10
        # score += (open_eat_move + player_eat + 1) ** 7

    if open_get_eat_move:
        score -= eat_value(open_get_eat_move + enemy_eat) / 10
        # score -= (open_get_eat_move + enemy_eat + 1) ** 7

    return score, l_eating_enemy, r_eating_enemy


@njit("UniTuple(int64[:], 2)(int64[:,:], int64, int64)", fastmath=True)
def get_diags(board, row_index, col_index):
    lr_diags = np.diag(board, col_index - row_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    return lr_diags, rl_diags

@njit
# @njit("Tuple((int64, List(int64[:])))(int64[:,:], int64[:], boolean, int64, int64, int64)", fastmath=True)
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    print(position)
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position

    lr_diags, rl_diags = get_diags(board, row_index, col_index)
    rows = board[row_index, :]
    columns = board[:, col_index]
    
    captured_stones = []

    result_lr, capture_left_lr, capture_right_lr = check_line(lr_diags, row_index, player, player_eat, enemy_eat)
    result_rl, capture_left_rl, capture_right_rl = check_line(rl_diags, row_index, player, player_eat, enemy_eat)
    result_row, capture_left_row, capture_right_row = check_line(rows, col_index, player, player_eat, enemy_eat)
    result_col, capture_left_col, capture_right_col = check_line(columns, row_index, player, player_eat, enemy_eat)

    score = result_lr + result_rl + result_row + result_col

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