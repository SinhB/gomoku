import numpy as np
import numba as nb
from numba import njit
from board_utils import get_vectors
from get_threats import check_line

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

class ForbiddenMove(Exception):
    def __init__(self):
        self.message = "Double free three is forbidden"

def init_board(size):
    board = np.zeros((size, size), dtype=np.int64)
    return board

def update_board(board, eating_left, eating_right, position, step_x, step_y, eaten_pos):
    if eating_left:
        board[position[0] - step_x][position[1] - step_y] = 0
        board[position[0] - 2 * step_x][position[1] - 2 * step_y] = 0
        eaten_pos.append([position[0] - step_x, position[1] - step_y])
        eaten_pos.append([position[0] - 2 * step_x, position[1] - 2 * step_y])
    if eating_right:
        board[position[0] + step_x][position[1] + step_y] = 0
        board[position[0] + 2 * step_x][position[1] + 2 * step_y] = 0
        eaten_pos.append([position[0] + step_x, position[1] + step_y])
        eaten_pos.append([position[0] + 2 * step_x, position[1] + 2 * step_y])
    
    return board, eaten_pos

def place_stone(board, position, player):
    row_index = position[0]
    col_index = position[1]

    lr_starting_index = col_index if row_index > col_index else row_index
    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index

    lr_diags, rl_diags, row, column = get_vectors(board, row_index, col_index)

    # Check only for open three because open_three + open_four isn't considered as a forbidden move
    _, lr_l_eating, lr_r_eating, _, _, _, _, _, lr_open_three, _, _, _, _ = check_line(lr_diags, lr_starting_index, player)
    _, rl_l_eating, rl_r_eating, _, _, _, _, _, rl_open_three, _, _, _, _ = check_line(rl_diags, rl_starting_index, player)
    _, row_l_eating, row_r_eating, _, _, _, _, _, row_open_three, _, _, _, _ = check_line(row, col_index, player)
    _, col_l_eating, col_r_eating, _, _, _, _, _, col_open_three, _, _, _, _ = check_line(column, row_index, player)

    if lr_open_three + rl_open_three + row_open_three + col_open_three >= 2:
        raise ForbiddenMove()

    board[row_index][col_index] = player

    total_eat = lr_l_eating + lr_r_eating + rl_l_eating + rl_r_eating + row_l_eating + row_r_eating + col_l_eating + col_r_eating
    print(lr_l_eating, lr_r_eating, rl_l_eating, rl_r_eating, row_l_eating, row_r_eating, col_l_eating, col_r_eating)
    eaten_pos = []

    # Check lr diag
    board, eaten_pos = update_board(board, lr_l_eating, lr_r_eating, position, 1, 1, eaten_pos)

    # Check rl diag
    board, eaten_pos = update_board(board, rl_l_eating, rl_r_eating, position, 1, -1, eaten_pos)

    # Check row diag
    board, eaten_pos = update_board(board, row_l_eating, row_r_eating, position, 0, 1, eaten_pos)

    # Check col diag
    board, eaten_pos = update_board(board, col_l_eating, col_r_eating, position, 1, 0, eaten_pos)
    print(eaten_pos)

    return board, total_eat, eaten_pos

def add_stone(board, player, position, captured_stones):
    """Add stone that is eating and replace the eaten stones"""
    board[position[0]][position[1]] = player
    for stone in captured_stones:
        board[stone[0]][stone[1]] = 0
    return board

def remove_stone(board, player, position, captured_stones):
    """Remove stone that ate players and replace the eaten player"""
    board[position[0]][position[1]] = 0
    for stone in captured_stones:
        board[stone[0]][stone[1]] = -player
    return board

def print_board(board, last_move=None):
    row_len, col_len = board.shape
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    
    print("  0 1 2 3 4 5 6 7 8 9 A B C D E F G H I")
    for i in range(0, row_len):
        line = f'{index[i]} '
        for j in range(0, col_len):
            if board[i][j] == 1:
                if type(last_move) == np.ndarray and i == last_move[0] and j == last_move[1]:
                    line += f'{bcolors.FAIL}N{bcolors.ENDC} '
                else:
                    line += f'{bcolors.OKBLUE}N{bcolors.ENDC} '
            elif board[i][j] == -1:
                if type(last_move) == np.ndarray and i == last_move[0] and j == last_move[1]:
                    line += f'{bcolors.FAIL}B{bcolors.ENDC} '
                else:
                    line += f'{bcolors.OKGREEN}B{bcolors.ENDC} '
            else:
                line += '- '
        print(line)
    print()