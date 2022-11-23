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

def init_board(size):
    board = np.zeros([size, size], dtype=np.int)
    return board

def place_stone(board, position, color):
    board[position[0]][position[1]] = color
    return board

def remove_stone(board, position, color):
    board[position[0]][position[1]] = 0
    return board

def print_board(board):
    line = ''
    row_len, col_len = board.shape
    for i in range(0, row_len):
        for j in range(0, col_len):
            if board[i][j] == 1:
                line += f'{bcolors.OKBLUE}N{bcolors.ENDC} '
            elif board[i][j] == -1:
                line += f'{bcolors.OKGREEN}B{bcolors.ENDC} '
            else:
                line += '- '
        print(line)
        line = ''
    print()