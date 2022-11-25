import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class NotEmptyPlaceError(Exception):

    def __init__(self, position):
        self.message = f"Tried to place a piece in a non empty place at coordinates {position}"
        super().__init__(self.message)

def init_board(size):
    blanc = 1<<(size * size + 1)
    noir = 1<<(size * size + 1)
    return blanc, noir

def place_stone(board1, board2, position):
    bit_index = position[0] * 19 + position[1]
    if board1[bit_index] or board2[bit_index]:
        raise NotEmptyPlace(position)
    board1[bit_index] = 1
    return board1, board2

def remove_stone(board1, board2, position, color):
    bit_index = position[0] * 19 + position[1]
    if board1[bit_index] or board2[bit_index]:
        raise NotEmptyPlace(position)
    board1[bit_index] = 0
    return board1, board2

def print_board(b_board, n_board, available_pos=None):
    line = ''
    b_board = bin(b_board)[3:]
    n_board = bin(n_board)[3:]
    for i in range(0, len(b_board)):
        if b_board[i] == '1':
            line += f'{bcolors.OKBLUE}B{bcolors.ENDC} '
        elif n_board[i] == '1':
            line += f'{bcolors.OKGREEN}N{bcolors.ENDC} '
        elif available_pos and i in available_pos:
            line += f'{bcolors.WARNING}A{bcolors.ENDC} '
        else:
            line += '- '
        if (i + 1) % 19 == 0:
            print(line)
            line = ''
    print()

def get_available_positions(b_board, n_board):
    list_of_pawns = []

    for i in range(0, len(b_board)):
        if b_board[i] == 1 or n_board[i] == 1:
            list_of_pawns.append(i)
    
    available_pos = []
    for pos in list_of_pawns:
        if pos > 0 and pos % 19 != 0:
            available_pos.append(pos - 1)
        
        if pos < 360 and (pos + 1) % 19 != 0:
            available_pos.append(pos + 1)

        if pos < 361 - 19:
            if not (pos + 1) % 19 == 0:
                available_pos.append(pos + 20)
            if not (pos) % 19 == 0:
                available_pos.append(pos + 18)

            available_pos.append(pos + 19)
        
        if pos > 18:
            if not (pos + 1) % 19 == 0:
                available_pos.append(pos - 18)
            if not (pos) % 19 == 0:
                available_pos.append(pos - 20)

            available_pos.append(pos - 19)

    available_pos = list(set(available_pos).difference(set(list_of_pawns)))
    
    # board_functions.print_board(b_board, n_board, available_pos)

    return available_pos



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
        # print(f"{i}({shift}) : {player_board[index]}, {enemy_board[index]} ({index})")
        if not break_left and not (l_index % 19 == 0 or l_index < 0 or l_index > 360):
            if l_is_consecutive:
                if player_board[index] == 1:
                    l_consecutive += 1
                else:
                    l_is_consecutive = False

            if l_check_eating_enemy or l_check_open_eating_move:
                if player_board[index] == 1 and l_consecutive_enemy == 2:
                    # Return eating_move
                    return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': True, 'open_eating_move': False, 'consecutive_enemy': 0}
                elif player_board[index] == 0 and enemy_board[index] == 0 and l_consecutive_enemy == 2:
                    # Return open_eating_move
                    return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': False, 'open_eating_move': True, 'consecutive_enemy': 0}
                elif enemy_board[index] == 1:
                    l_consecutive_enemy += 1
                else:
                    l_check_eating_enemy = False
                    l_check_open_eating_move = False

            if player_board[index] == 0 and enemy_board[index] == 0 :
                if is_after_one_zero:
                    break_left = True
            else:
                l_is_after_one_zero = True
            
            if l_is_after_one_zero:
                if player_board[index] == 1:
                    l_additional += 1

            index_left -= shift
        if not break_right and not (r_index % 19 == 0 or r_index < 0 or r_index > 360):
            if r_is_consecutive:
                if player_board[index] == 1:
                    r_consecutive += 1
                else:
                    r_is_consecutive = False

            if r_check_eating_enemy or r_check_open_eating_move:
                if player_board[index] == 1 and r_consecutive_enemy == 2:
                    # Return eating_move
                    return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': True, 'open_eating_move': False, 'consecutive_enemy': 0}
                elif player_board[index] == 0 and enemy_board[index] == 0 and r_consecutive_enemy == 2:
                    # Return open_eating_move
                    return {'consecutive' : 0, 'additional': 0, 'empty_space': False, 'eating_enemy': False, 'open_eating_move': True, 'consecutive_enemy': 0}
                elif enemy_board[index] == 1:
                    r_consecutive_enemy += 1
                else:
                    r_check_eating_enemy = False
                    r_check_open_eating_move = False

            if player_board[index] == 0 and enemy_board[index] == 0 :
                if r_is_after_one_zero:
                    break_right = True
            else:
                r_is_after_one_zero = True
            
            if r_is_after_one_zero:
                if player_board[index] == 1:
                    r_additional += 1

            index_right += shift
        
    return {
        'consecutive' : consecutive,
        'additional': additional,
        'empty_space': empty_space,
        'eating_enemy': eating_enemy,
        'open_eating_move': open_eating_move,
        'consecutive_enemy': consecutive_enemy
    }