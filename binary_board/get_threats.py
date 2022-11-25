import functools

from board_functions import bcolors

def get_new_threats(player_board, enemy_board, position, maximizing_player):
    score = 0
    score += check_line(player_board, enemy_board, position, 'lr_diags', maximizing_player)
    score += check_line(player_board, enemy_board, position, 'rl_diags', maximizing_player)
    score += check_line(player_board, enemy_board, position, 'rows', maximizing_player)
    score += check_line(player_board, enemy_board, position, 'columns', maximizing_player)
    # print(f"Total score : {score}")
    return score

def check_side(player_board, enemy_board, position, shift):
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

    index_left = position - shift
    index_right = position + shift

    for i in range(0, 5):
        print(player_board[index_left], player_board[index_right])
        print(type(player_board[index_left]), type(player_board[index_right]))
        print()
        # if is_consecutive:
            # if player_board[index_left] == 1:


        index_left -= shift
        index_right += shift
        
    return {
        'consecutive' : consecutive,
        'additional': additional,
        'empty_space': empty_space,
        'eating_enemy': eating_enemy,
        'open_eating_move': open_eating_move,
        'consecutive_enemy': consecutive_enemy
    }

# @functools.cache
def check_line(player_board, enemy_board, position, line, maximizing_player):
    if line == 'lr_diags':
        l_analysis, r_analysis = check_side(player_board, enemy_board, position, 20)
    elif line == 'rl_diags':
        l_analysis, r_analysis = check_side(player_board, enemy_board, position, 18)
    elif line == 'rows':
        l_analysis, r_analysis = check_side(player_board, enemy_board, position, 1)
    elif line == 'columns':
        l_analysis, r_analysis = check_side(player_board, enemy_board, position, 19)


    # print(l_analysis)
    # print(r_analysis)
    score = 0
    total_consecutive = l_analysis['consecutive'] + r_analysis['consecutive']
    total_consecutive_enemy = l_analysis['consecutive_enemy'] + r_analysis['consecutive_enemy']

    # print(f"TOTAL ME : {total_consecutive}")
    # print(f"TOTAL ENEMY : {total_consecutive_enemy}")
    if total_consecutive == 4:
        # Win
        score += 100_000_000
    
    if total_consecutive_enemy == 4:
        # Block enemy win
        score += 90_000_000
    
    if total_consecutive == 3 and l_analysis['empty_space'] and r_analysis['empty_space']:
        # 4 in a row with an open room on each side
        score += 80_000_000

    if total_consecutive_enemy == 3 and l_analysis['empty_space'] and r_analysis['empty_space']:
        # 4 in a row with an open room on each side for the enemy
        score += 80_000_000

    if total_consecutive == 3:
        score += 100_000

    if total_consecutive == 2:
        score += 1_000
    
    if total_consecutive == 1:
        score += 100
    
    if l_analysis['eating_enemy'] and r_analysis['eating_enemy']:
        score += 5_000_000
    elif l_analysis['eating_enemy'] or r_analysis['eating_enemy']:
        score += 1_000_000
    
    if l_analysis['open_eating_move'] and r_analysis['open_eating_move']:
        score += 1_000_000
    elif l_analysis['open_eating_move'] or r_analysis['open_eating_move']:
        score += 500_000

    if total_consecutive_enemy == 4:
        score += 90_000_000

    # print(score)
    return score