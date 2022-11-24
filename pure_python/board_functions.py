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


def check_eating_enemy(board, position, step_x, step_y, player):
    left = [position[0] - step_x, position[1] - step_y]
    right = [position[0] + step_x, position[1] + step_y]
    enemy = player * -1

    eating_left = False
    eating_right = False

    consecutive_enemy = 0
    for i in range(0, 3):
        if left[0] >= 0 and left[1] >= 0 and left[0] <= 18 and left[1] <= 18:
            if board[left[0]][left[1]] == player and consecutive_enemy == 2:
                board[left[0] + step_x][left[1] + step_y] = 0
                board[left[0] + 2 * step_x][left[1] + 2 * step_y] = 0
                eating_left = True
                break
            elif board[left[0]][left[1]] == enemy:
                consecutive_enemy += 1
            else:
                break
        left[0] -= step_x
        left[1] -= step_y

    consecutive_enemy = 0
    for i in range(0, 3):
        if right[0] >= 0 and right[1] >= 0 and right[0] <= 18 and right[1] <= 18:
            if board[right[0]][right[1]] == player and consecutive_enemy == 2:
                board[right[0] - step_x][right[1] - step_y] = 0
                board[right[0] - 2 * step_x][right[1] - 2 * step_y] = 0
                eating_right = True
                break
            elif board[right[0]][right[1]] == enemy:
                consecutive_enemy += 1
            else:
                break
        right[0] += step_x
        right[1] += step_y
    return eating_left, eating_right

def update_board(board, eating_left, eating_right, position, step_x, step_y):
    if eating_left:
        board[position[0] - step_x][position[1] - step_y] = 0
        board[position[0] - 2 * step_x][position[1] - 2 * step_y] = 0
    
    if eating_right:
        board[position[0] + step_x][position[1] + step_y] = 0
        board[position[0] + 2 * step_x][position[1] + 2 * step_y] = 0
    
    return board

def place_stone(board, position, player):
    board[position[0]][position[1]] = player
    total_eat = 0
    # Check lr diag
    eating_left, eating_right = check_eating_enemy(board, position, -1, -1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, -1, -1)
    
    # Check rl diag
    eating_left, eating_right = check_eating_enemy(board, position, 1, 1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 1, 1)
    
    # Check row diag
    print("\n\nCHECK ROW")
    print(position)
    eating_left, eating_right = check_eating_enemy(board, position, 0, 1, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 0, 1)
    print("END CHECK ROW\n\n")
    
    # Check col diag
    eating_left, eating_right = check_eating_enemy(board, position, 1, 0, player)
    total_eat += eating_left + eating_right
    board = update_board(board, eating_left, eating_right, position, 1, 0)

    return board, total_eat

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