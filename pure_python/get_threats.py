import get_lines
import functools
from operator import add

def get_new_threats(board, row_index, col_index, maximizing_player, player, total_eat):
    lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    result_lr = check_line(tuple(lr_diags), row_index, maximizing_player, player)
    result_rl = check_line(tuple(rl_diags), row_index, maximizing_player, player)
    result_row = check_line(tuple(rows), col_index, maximizing_player, player)
    result_col = check_line(tuple(columns), row_index, maximizing_player, player)

    total_threat = [sum(x) for x in zip(result_lr, result_rl, result_row, result_col)]

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
        eat_move,
        open_eat_move,
        open_get_eat_move
    ) = total_threat

    score = 1
    i = 0
    print_score = False
    if print_score:
        print(f"Score 1 : {score}")

    # Player series
    score += closed_two * 10
    if print_score:
        print(f"Score 2 : {score}")
    score += semi_close_two * 50
    if print_score:
        print(f"Score 3 : {score}")
    score += open_two * 500
    if print_score:
        print(f"Score 4 : {score}")

    score += closed_three * 20
    if print_score:
        print(f"Score 5 : {score}")
    score += semi_closed_three * 100
    if print_score:
        print(f"Score 6 : {score}")
    score += open_three * 1_000
    if print_score:
        print(f"Score 7 : {score}")

    score += closed_four * 40
    if print_score:
        print(f"Score 8 : {score}")
    score += semi_closed_four * 200
    if print_score:
        print(f"Score 9 : {score}")
    score += open_four * 2_000
    if print_score:
        print(f"Score 10 : {score}")

    score += five * 100_000_000
    if print_score:
        print(f"Score 11 : {score}")

    # Enemy series
    score += enemy_closed_two * 5
    if print_score:
        print(f"Score 12 : {score}")
    score += enemy_semi_close_two * 15
    if print_score:
        print(f"Score 13 : {score}")
    score += enemy_open_two * 250
    if print_score:
        print(f"Score 14 : {score}")

    score += enemy_closed_three * 10
    if print_score:
        print(f"Score 15 : {score}")
    score += enemy_semi_closed_three * 50
    if print_score:
        print(f"Score 16 : {score}")
    score += enemy_open_three * 4_000
    if print_score:
        print(f"Score 17 : {score}")

    score += enemy_closed_four * 20
    if print_score:
        print(f"Score 18 : {score}")
    score += enemy_semi_closed_four * 1_000_000
    # if enemy_semi_closed_four:
    #     print(f"enemy_semi_closed_four : {enemy_semi_closed_four}")
    if print_score:
        print(f"Score 19 : {score}")
    score += enemy_open_four * 1_000_000
    if print_score:
        print(f"Score 20 : {score}")


    # Eating move
    score -= open_get_eat_move * 200
    if print_score:
        print(f"Score 21 : {score}")
    score += open_eat_move * 200
    if print_score:
        print(f"Score 22 : {score}")
    score += (eat_move + total_eat) ** 10
    if print_score:
        print(f"Score 23 : {score}")

    return score if maximizing_player else score * -1

def check_side(side, player=0):
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
                return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': True, 'open_eating_move': False, 'consecutive_enemy': 0}
            elif side[i] == 0 and consecutive_enemy == 2:
                # Return open_eating_move
                return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': False, 'open_eating_move': True, 'consecutive_enemy': 0}
            elif side[i] == player * -1:
                consecutive_enemy += 1
            else:
                check_eating_enemy = False
                check_open_eating_move = False

        if side[i] == 0:
            if consecutive > 0 or consecutive_enemy > 0:
                empty_space = True
            if is_after_one_zero:
                break
            else:
                is_after_one_zero = True
        
        if is_after_one_zero:
            if side[i] == player:
                additional += 1
        
    return {
        'consecutive' : consecutive,
        'additional': additional,
        'empty_space': empty_space,
        'eating_enemy': eating_enemy,
        'open_eating_move': open_eating_move,
        'consecutive_enemy': consecutive_enemy
    }

@functools.cache
def check_line(line, starting_index, maximizing_player, player):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    # print(f"left : {left}")
    # print(f"right : {right}")
    # print()

    l_analysis = check_side(left, player)
    r_analysis = check_side(right, player)

    total_consecutive = l_analysis['consecutive'] + r_analysis['consecutive']
    total_consecutive_enemy = l_analysis['consecutive_enemy'] + r_analysis['consecutive_enemy']
    total_empty_space = l_analysis['empty_space'] + r_analysis['empty_space']

    eat_move = l_analysis['eating_enemy'] + r_analysis['eating_enemy']
    open_eat_move = l_analysis['open_eating_move'] + r_analysis['open_eating_move']
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

    elif total_consecutive == 4:
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


    if total_consecutive_enemy == 1:
        if total_empty_space == 2:
            enemy_closed_two += 1
        elif total_empty_space == 1:
            enemy_semi_close_two += 1
        else:
            enemy_open_two += 1

    elif total_consecutive_enemy == 3:
        if total_empty_space == 2:
            enemy_closed_three += 1
        elif total_empty_space == 1:
            enemy_semi_closed_three += 1
        else:
            enemy_open_three += 1

    elif total_consecutive_enemy == 4:
        if total_empty_space == 2:
            enemy_closed_four += 1
        elif total_empty_space == 1:
            enemy_semi_closed_four += 1
        else:
            enemy_open_four += 1

    # if     total_consecutive_enemy = l_analysis['consecutive_enemy'] + r_analysis['consecutive_enemy']


    # print(f"total_consecutive: {total_consecutive}")
    # print(f"total_consecutive_enemy: {total_consecutive_enemy}")
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
        eat_move,
        open_eat_move,
        open_get_eat_move
    )