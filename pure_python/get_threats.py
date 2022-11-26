import get_lines
import functools
from operator import add

# Player series multiplicator
multiplicator_closed_two = 10
multiplicator_semi_close_two = 50
multiplicator_open_two = 500

multiplicator_closed_three = 20
multiplicator_semi_closed_three = 1_000
multiplicator_open_three = 10_000

multiplicator_closed_four = 40
multiplicator_semi_closed_four = 20_000
multiplicator_open_four = 100_000

multiplicator_five = 100_000_000

# Block enemy series multiplicator
multiplicator_enemy_closed_two = 20
multiplicator_enemy_semi_close_two = 100
multiplicator_enemy_open_two = 1000

multiplicator_enemy_closed_three = 40
multiplicator_enemy_semi_closed_three = 2_000
multiplicator_enemy_open_three = 400_000

multiplicator_enemy_closed_four = 80
multiplicator_enemy_semi_closed_four = 1_000_000
multiplicator_enemy_open_four = 5_000_000

enemy_multiplicator_five = 50_000_000

# Eating move
multiplicator_open_eat_move = 200

def get_new_threats(board, position, maximizing_player, player, total_eat):
    if not maximizing_player:
        player = player * -1

    row_index = position[0]
    col_index = position[1]

    lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    result_lr = check_line(tuple(lr_diags), row_index, player)
    result_rl = check_line(tuple(rl_diags), row_index, player)
    result_row = check_line(tuple(rows), col_index, player)
    result_col = check_line(tuple(columns), row_index, player)

    (
        closed_two,
        semi_close_two,
        open_two,
        closed_three,
        semi_closed_three,
        open_three,
        closed_four,
        semi_closed_four,
        open_four,
        five,
        enemy_closed_two,
        enemy_semi_close_two,
        enemy_open_two,
        enemy_closed_three,
        enemy_semi_closed_three,
        enemy_open_three,
        enemy_closed_four,
        enemy_semi_closed_four,
        enemy_open_four,
        enemy_five,
        eat_move,
        open_eat_move,
        open_get_eat_move
    ) = [sum(x) for x in zip(result_lr, result_rl, result_row, result_col)]

    if open_three > 2 or (open_get_eat_move > 0 and total_eat[player * -1] >= 4):
        return 0

    score = 1

    # Player series
    score += closed_two * multiplicator_closed_two
    score += semi_close_two * multiplicator_semi_close_two
    score += open_two * multiplicator_open_two

    score += closed_three * multiplicator_closed_three
    score += semi_closed_three * multiplicator_semi_closed_three
    score += open_three * multiplicator_open_three

    score += closed_four * multiplicator_closed_four
    score += semi_closed_four * multiplicator_semi_closed_four
    score += open_four * multiplicator_open_four

    score += five * multiplicator_five

    # Enemy series
    score += enemy_closed_two * multiplicator_enemy_closed_two
    score += enemy_semi_close_two * multiplicator_enemy_semi_close_two
    score += enemy_open_two * multiplicator_enemy_open_two

    score += enemy_closed_three * multiplicator_enemy_closed_three
    score += enemy_semi_closed_three * multiplicator_enemy_semi_closed_three
    score += enemy_open_three * multiplicator_enemy_open_three

    score += enemy_closed_four * multiplicator_enemy_closed_four
    score += enemy_semi_closed_four * multiplicator_enemy_semi_closed_four
    score += enemy_open_four * multiplicator_enemy_open_four

    score += enemy_five * enemy_multiplicator_five


    # Eating move
    if eat_move:
        score += (eat_move + total_eat[player] + 1) ** 10

    if open_get_eat_move:
        score -= (open_get_eat_move + total_eat[player * -1]) ** 10

    if open_eat_move:
        score += open_eat_move * multiplicator_open_eat_move

    # return score
    return score if maximizing_player else score * -1

def check_side(side, player):
    # Number of consecutive pawn placed directly next to the one played
    consecutive = 0
    # Number of enemy consecutive pawn placed directly next to the one played
    consecutive_enemy = 0
    # Number of consecutive pawn separated by one zero from the consecutive ones
    additional = 0
    # Is there an empty space at the end of the last serie of pawn
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

        if check_eating_enemy or check_open_eating_move and not is_after_one_zero:
            if side[i] == player and consecutive_enemy == 2:
                # Return eating_move
                return 0, 0, False, True, False, 0
            elif side[i] == 0 and consecutive_enemy == 2:
                # Return open_eating_move
                return 0, 0, False, False, True, 0
            elif side[i] == player * -1:
                consecutive_enemy += 1
            else:
                check_eating_enemy = False
                check_open_eating_move = False

        if side[i] == 0:
            if i == 0 or consecutive > 0 or consecutive_enemy > 0:
                empty_space = True
            if is_after_one_zero:
                break
            else:
                is_after_one_zero = True
        
        if is_after_one_zero:
            if side[i] == player:
                additional += 1
        
    return consecutive, additional, empty_space, eating_enemy, open_eating_move, consecutive_enemy

# @functools.cache
def check_line(line, starting_index, player):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]

    l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_consecutive_enemy = check_side(left, player)
    r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_consecutive_enemy = check_side(right, player)

    total_consecutive = l_consecutive + r_consecutive
    total_consecutive_enemy = l_consecutive_enemy + r_consecutive_enemy
    total_empty_space = l_empty_space + r_empty_space
    # print(f"? = {total_consecutive_enemy}")

    eat_move = l_eating_enemy + r_eating_enemy
    open_eat_move = l_open_eating_move + r_open_eating_move
    open_get_eat_move = 0

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

    if l_consecutive + l_additional:
        open_three += 1
    if r_consecutive + r_additional:
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
            closed_three += 1
        elif total_empty_space == 1:
            semi_closed_three += 1
        else:
            open_three += 1

    elif total_consecutive == 3:
        if total_empty_space == 2:
            closed_four += 1
        elif total_empty_space == 1:
            semi_closed_four += 1
        else:
            open_four += 1

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

    if total_consecutive_enemy == 2:
        if total_empty_space == 2:
            enemy_open_two += 1
        elif total_empty_space == 1:
            enemy_semi_close_two += 1
        else:
            enemy_closed_two += 1

    elif total_consecutive_enemy == 3:
        if total_empty_space == 2:
            enemy_open_three += 1
        elif total_empty_space == 1:
            enemy_semi_closed_three += 1
        else:
            enemy_closed_three += 1

    elif total_consecutive_enemy == 4:
        if total_empty_space == 2:
            enemy_open_four += 1
        elif total_empty_space == 1:
            enemy_semi_closed_four += 1
        else:
            enemy_closed_four += 1

    elif total_consecutive >= 4:
        enemy_five += 1

    return (
        closed_two,
        semi_close_two,
        open_two,
        closed_three,
        semi_closed_three,
        open_three,
        closed_four,
        semi_closed_four,
        open_four,
        five,
        enemy_closed_two,
        enemy_semi_close_two,
        enemy_open_two,
        enemy_closed_three,
        enemy_semi_closed_three,
        enemy_open_three,
        enemy_closed_four,
        enemy_semi_closed_four,
        enemy_open_four,
        enemy_five,
        eat_move,
        open_eat_move,
        open_get_eat_move
    )