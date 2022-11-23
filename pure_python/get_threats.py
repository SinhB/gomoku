import get_lines
import functools

def get_new_threats(board, row_index, col_index, maximizing_player, player):
    lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    rows = get_lines.get_position_rows(board, row_index)
    columns = get_lines.get_position_columns(board, col_index)

    score = 0
    # lr_analysis = check_line(tuple(lr_diags), row_index, maximizing_player, player)
    # rl_analysis = check_line(tuple(rl_diags), row_index, maximizing_player, player)
    # row_analysis = check_line(tuple(rows), col_index, maximizing_player, player)
    # col_analysis = check_line(tuple(columns), row_index, maximizing_player, player)

    score += check_line(tuple(lr_diags), row_index, maximizing_player, player)
    score += check_line(tuple(rl_diags), row_index, maximizing_player, player)
    score += check_line(tuple(rows), col_index, maximizing_player, player)
    score += check_line(tuple(columns), row_index, maximizing_player, player)

    # win = True if lr_analysis['win'] or rl_analysis['win'] or row_analysis['win'] or col_analysis['win'] else False
    # overall_data = {
    #     "win": win,
    #     "open_four": 0,
    #     "open_three": 0,
    #     "closed_three": 0,
    #     "open_double": 0,
    #     "closed_double": 0,
    # }

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

        if check_eating_enemy or check_open_eating_move:
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

    l_analysis = check_side(left, player)
    r_analysis = check_side(right, player)

    # total_consecutive = l_analysis['consecutive'] + r_analysis['consecutive']

    # line_analysis = {}

    # if total_consecutive == 4 and (l_analysis['empty_space'] or r_analysis['empty_space']):
    #     line_analysis['win'] = True
    #     "open_three": True if total_consecutive == 2 and l_analysis['empty_space'] and r_analysis['empty_space'],
    #     "open_two"

    # return line_analysis
    l_consecutive, l_additional, l_empty_space, l_eating_enemy, l_open_eating_move, l_consecutive_enemy = check_side(left, player)
    r_consecutive, r_additional, r_empty_space, r_eating_enemy, r_open_eating_move, r_consecutive_enemy = check_side(right, player)

    score = 0
    total_consecutive = l_analysis['consecutive'] + r_analysis['consecutive']
    total_consecutive_enemy = l_analysis['consecutive_enemy'] + r_analysis['consecutive_enemy']

    if total_consecutive == 4:
        # Win
        return 100_000_000
    
    if total_consecutive_enemy == 4:
        # Block enemy win
        return 90_000_000

    if total_consecutive_enemy == 3 and l_analysis['empty_space'] and r_analysis['empty_space']:
        # 4 in a row with an open room on each side for the enemy
        return 80_000_000
        # score += 80_000_000

    if total_consecutive == 3 and l_analysis['empty_space'] and r_analysis['empty_space']:
        # 4 in a row with an open room on each side
        return 80_000_000
        # score += 80_000_000

    if total_consecutive == 3:
        return 100_000
        # score += 100_000

    if total_consecutive == 2:
        return 1_000
        # score += 1_000
    
    if total_consecutive == 1:
        return 100
        # score += 100
    
    if l_analysis['eating_enemy'] and r_analysis['eating_enemy']:
        return 5_000_000
        # score += 5_000_000
    elif l_analysis['eating_enemy'] or r_analysis['eating_enemy']:
        return 1_000_000
        # score += 1_000_000
    
    if l_analysis['open_eating_move'] and r_analysis['open_eating_move']:
        return 1_000_000
        # score += 1_000_000
    elif l_analysis['open_eating_move'] or r_analysis['open_eating_move']:
        return 500_000
        # score += 500_000

    if total_consecutive_enemy == 4:
        return 90_000_000
        score += 90_000_000

    return 1