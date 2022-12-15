import get_lines
import functools
from operator import add
import numba as nb
import numpy as np
from numba import njit, prange, int64, typeof
from numba.types import bool_

print_values = False
print_values = True

@njit("(int64)(int64)", fastmath=True)
def eat_value(eat_number):
    if eat_number == 0:
        return 0
    elif eat_number == 1:
        return 20_000 
    elif eat_number == 2:
        return 30_000
    elif eat_number == 3:
        return 40_000
    elif eat_number == 4:
        return 90_000
    # Win by capture
    return 3_000_000


multiplicator_five = 200_000
multiplicator_enemy_five = 100_000

multiplicator_enemy_open_four = 40_000
multiplicator_enemy_semi_closed_four = 40_000

multiplicator_open_four = 35_000

multiplicator_enemy_open_three = 40_000
multiplicator_open_three = 1_000

multiplicator_semi_closed_four = 2_000
multiplicator_enemy_semi_closed_three = 1_000
multiplicator_semi_closed_three = 500
multiplicator_open_two = 20
multiplicator_semi_closed_two = 100
multiplicator_enemy_semi_closed_two = 100
multiplicator_enemy_open_two = 10

@njit("Tuple((int64, int64, boolean, boolean, boolean, boolean, int64, int64))(int64[:], int64)", fastmath=True)
def check_side(side, player):
    is_consecutive = True
    consecutive_value = False
    consecutive_count = 0

    is_additional = False
    additional_value = False
    additional_count = 0

    is_blocked = False

    is_after_one_zero = False

    empty_space = True

    for i in range(0, min(len(side), 6)):
        if is_consecutive:
            if side[i] == 0:
                is_consecutive = False
                is_after_one_zero = True
            elif consecutive_value == False:
                consecutive_value = side[i]
                consecutive_count += 1
            elif side[i] == consecutive_value:
                consecutive_count += 1
            else:
                empty_space = False
                is_additional = True
                is_consecutive = False
                additional_value = side[i]
                additional_count += 1

        elif is_after_one_zero:
            if side[i] == 0:
                break
            else:
                is_additional = True
                additional_value = side[i]
                additional_count += 1
        
        elif is_additional:
            if side[i] == additional_value:
                additional_count += 1
            else:
                break

    if consecutive_value != False:
        consecutive = consecutive_count if consecutive_value == player else 0
        consecutive_enemy = consecutive_count if consecutive_value == player * -1 else 0
    else:
        consecutive = 0
        consecutive_enemy = 0

    if additional_value != False:
        additional = additional_count if additional_value == player else 0
        additional_enemy = additional_count if additional_value == player * -1 else 0
    else:
        additional = 0
        additional_enemy = 0

    if print_values:
        print(player, consecutive_value, consecutive_count, is_after_one_zero, additional_value)
    if consecutive_value == player * -1 and consecutive_count == 2:
        open_eating_move = True if is_after_one_zero else False
        if not is_after_one_zero and additional_value == player:
            eating_enemy = True
            empty_space = True
        else:
            eating_enemy = False
        open_get_eat_move = False

    elif consecutive_value == player and consecutive_count == 2 and is_after_one_zero:
        open_get_eat_move = True

    else:
        eating_enemy = False
        open_eating_move = False
        open_get_eat_move = False

    return consecutive, additional, empty_space, eating_enemy, open_eating_move, open_get_eat_move, consecutive_enemy, additional_enemy

# @functools.cache
# @njit("UniTuple(int64, 23)(int64[:], int64, int64)", fastmath=True)
@njit("Tuple((int64, boolean, boolean, int64))(int64[:], int64, int64, int64, int64)", fastmath=True)
def check_line(line, starting_index, player, player_eat, enemy_eat):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    if print_values:
        print(line)
        print(left, right)

    l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_open_get_eat_move, l_consecutive_enemy, l_additional_enemy = check_side(left, player)
    if print_values:
        print(l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_open_get_eat_move, l_consecutive_enemy, l_additional_enemy)
    r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_open_get_eat_move, r_consecutive_enemy, r_additional_enemy = check_side(right, player)
    if print_values:
        print(r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_open_get_eat_move, r_consecutive_enemy, r_additional_enemy)
        # print("\n")

    total_consecutive = l_consecutive + r_consecutive
    total_consecutive_enemy = l_consecutive_enemy + r_consecutive_enemy
    total_empty_space = l_empty_space + r_empty_space

    # Player serie
    semi_closed_two = 0
    open_two = 0

    semi_closed_three = 0
    open_three = 0

    semi_closed_four = 0
    open_four = 0

    five = 0 if total_consecutive < 4 else 1

    # Enemy player serie
    enemy_semi_closed_two = 0
    enemy_open_two = 0

    enemy_semi_closed_three = 0
    enemy_open_three = 0

    enemy_semi_closed_four = 0
    enemy_open_four = 0

    enemy_five = 0 if total_consecutive_enemy < 4 else 1

    eat_move = l_eating_enemy + r_eating_enemy
    open_eat_move = l_open_eating_move + r_open_eating_move
    open_get_eat_move = l_open_get_eat_move + r_open_get_eat_move

    if l_additional != 0 and l_consecutive + l_additional == 2 and l_empty_space == True:
        open_three += 1

    if l_additional != 0 and l_consecutive + l_additional == 3 and l_empty_space == True:
        open_four += 1

    if r_empty_space:
        if r_additional == 0:
            if r_consecutive + r_additional == 2:
                open_three += 1
            if r_consecutive + r_additional == 3:
                open_four += 1
        if r_additional_enemy == 0:
            if r_consecutive_enemy + r_additional_enemy == 3:
                enemy_open_three += 1
            if r_consecutive_enemy + r_additional_enemy == 4:
                enemy_open_four += 1

    if l_empty_space:
        if l_additional == 0:
            if l_consecutive + l_additional == 2:
                open_three += 1
            if l_consecutive + l_additional == 3:
                open_four += 1
        if l_additional_enemy == 0:
            if l_consecutive_enemy + l_additional_enemy == 3:
                enemy_open_three += 1
            if l_consecutive_enemy + l_additional_enemy == 4:
                enemy_open_four += 1

    if total_empty_space == 2:
        # Open two
        if total_consecutive == 2:
            open_two += 1
        if total_consecutive_enemy == 2:
            enemy_open_two += 1

        # Open three
        if total_consecutive == 3:
            open_three += 1
        if total_consecutive_enemy == 3:
            enemy_open_three += 1

        # Open four
        if total_consecutive == 4:
            open_four += 1
        if total_consecutive_enemy == 4:
            enemy_open_four += 1
    elif total_empty_space == 1:
        # Semi closed two
        if total_consecutive == 2:
            semi_closed_two += 1
        if total_consecutive_enemy == 2:
            enemy_semi_closed_two += 1

        # Semi closed three
        if total_consecutive == 3:
            semi_closed_three += 1
        if total_consecutive_enemy == 3:
            enemy_semi_closed_three += 1

        # Semi closed four
        if total_consecutive == 4:
            semi_closed_four += 1
        if total_consecutive_enemy == 4:
            enemy_semi_closed_four += 1

    eat_score = eat_value(eat_move + player_eat) if eat_move else 0
    open_eat_score = eat_value(open_eat_move + player_eat - 1) if eat_move else 0
    open_get_eat_score = eat_value(open_get_eat_move + player_eat) if eat_move else 0

    score = 0
    if r_consecutive + l_consecutive >= 4:
        print("five")
        score = 1_000_000
    elif r_consecutive_enemy + l_consecutive_enemy >= 4:
        print("enemy five")
        score = 125_000
    elif enemy_semi_closed_four:
        print("enemy semi open four")
        score = 100_000
    elif enemy_open_three > 0:
        print("enemy open three")
        score = 90_000
    elif open_four > 0:
        print("open four")
        score = 80_000
    elif semi_closed_four > 0:
        print("semi open four")
        score = 75_000
    elif enemy_open_four > 0:
        print("enemy open four")
        score = 70_000
    elif semi_closed_two:
        # Avoid being eaten
        print("semi closed two")
        score = 65_000

    elif open_three > 0:
        print("open three")
        score = 60_000

    elif semi_closed_three:
        print("semi open three")
        score = 10_000
    elif enemy_semi_closed_three:
        print("enemy semi open three")
        score = 1_000
    elif open_two:
        print("open two")
        score = 1_000
    elif enemy_open_two > 0:
        print("enemy open two")
        score = 100


    score += eat_score + open_eat_score - open_get_eat_score
    print(score, eat_score, open_eat_score, open_get_eat_score)
    # if eat_move:
    #     score += eat_value(eat_move + player_eat)

    # if open_eat_move:
    #     score += eat_value(open_eat_move + player_eat - 1)

    # if open_get_eat_move:
    #     score -= eat_value(open_get_eat_move + enemy_eat)

    # print("five", five, "enemy_five", enemy_five)
    # print("open_four", open_four, "enemy_open_four", enemy_open_four)
    # print("semi_closed_four", semi_closed_four, "enemy_semi_closed_four", enemy_semi_closed_four)
    # print("open_three", open_three, "enemy_open_three", enemy_open_three)
    # print("semi_closed_three", semi_closed_three, "enemy_semi_closed_three", enemy_semi_closed_three)
    # print("open_two", open_two, "enemy_open_two", enemy_open_two)
    # print("semi_closed_two", semi_closed_two, "enemy_semi_closed_two", enemy_semi_closed_two)
    # print("eat_move", eat_move, "open_eat_move", open_eat_move, "open_get_eat_move", open_get_eat_move)

    return score, l_eating_enemy, r_eating_enemy, open_three


@njit("UniTuple(int64[:], 2)(int64[:,:], int64, int64)", fastmath=True)
def get_diags(board, row_index, col_index):
    lr_diags = np.diag(board, col_index - row_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    return lr_diags, rl_diags

@njit
# @njit("Tuple((int64, List(int64[:])))(int64[:,:], int64[:], boolean, int64, int64, int64)", fastmath=True)
def get_new_threats(board, position, maximizing_player, player, player_eat, enemy_eat, depth):
    if print_values:
        print(position)
    if not maximizing_player:
        player = player * -1

    row_index, col_index = position

    lr_diags, rl_diags = get_diags(board, row_index, col_index)
    rows = board[row_index, :]
    columns = board[:, col_index]
    
    captured_stones = []

    if print_values:
        print("LR")
    lr_starting_index = col_index if row_index > col_index else row_index
    result_lr, capture_left_lr, capture_right_lr, open_three_lr = check_line(lr_diags, lr_starting_index, player, player_eat, enemy_eat)
    if print_values:
        print("RL")
    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
    result_rl, capture_left_rl, capture_right_rl, open_three_rl = check_line(rl_diags, rl_starting_index, player, player_eat, enemy_eat)
    if print_values:
        print("ROW")
    result_row, capture_left_row, capture_right_row, open_three_row = check_line(rows, col_index, player, player_eat, enemy_eat)
    if print_values:
        print("COL")
    result_col, capture_left_col, capture_right_col, open_three_col = check_line(columns, row_index, player, player_eat, enemy_eat)

    if open_three_lr + open_three_rl + open_three_row + open_three_col >= 2:
        return 1_000_000 * -1 if maximizing_player else 1, captured_stones
    if print_values:
        print("\n")
        # print("\n")

    score = max([result_lr, result_rl, result_row, result_col])

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