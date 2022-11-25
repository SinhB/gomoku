import get_lines
from get_threats import get_new_threats 
import random
import time

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

def get_next_move(board, size, depth, maximizing_player, player, total_eat):
    alpha = -1_000_000_000
    beta = 1_000_000_000
    moves_results = minimax(board, depth, alpha, beta, maximizing_player, size, 0, depth, player, total_eat)
    moves_results.sort(key=lambda tup: tup[0], reverse=True)
    return moves_results[0][1]

def filter_pos(board, maximizing_player, player, size, total_eat):
    eval_to_pos = []
    start1 = time.time()
    available_pos = get_lines.get_available_positions(board, size)
    stop1 = time.time()
    print(f"get pos = {stop1 - start1}")

    if len(available_pos) == 0:
        return [([random.randint(6, 12), random.randint(6, 12)], 1)]
    
    start2 = time.time()
    eval_to_pos = [(p, get_new_threats(board, p, maximizing_player, player, total_eat[player])) for p in available_pos]
    stop2 = time.time()
    print(f"evaluat = {stop2 - start2}")

    eval_to_pos.sort(key=lambda tup: tup[1], reverse=maximizing_player)

    return eval_to_pos[:5]

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats, max_depth, player, total_eat):
    # print(current_threats)
    # if depth == 0 or is_finished():
    # print(f"current_threats : {current_threats} {depth}")
    if depth == 0 or current_threats >= 50_000_000 or current_threats <= -50_000_000:
        return current_threats

    best_position = filter_pos(board, maximizing_player, player, size, total_eat)

    if depth == max_depth:
        moves_results = []

    if maximizing_player:
        maxEval = -1_000_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = 1

            start1 = time.time()
            get_lines.get_new_positions(board, size, best_position, position)
            available_pos = get_lines.get_available_positions(board, size)
            stop1 = time.time()
            print(f"get new pos = {stop1 - start1}")

            evaluation = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats, max_depth, player, total_eat)
            # print(new_threats)
            if depth == max_depth:
                moves_results.append((evaluation, position))
            board[position[0]][position[1]] = 0

            maxEval = max(alpha, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                if depth == max_depth:
                    print(f"{bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        if depth == max_depth:
            return moves_results
        return maxEval

    else:
        minEval = 1_000_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = -1

            evaluation = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats, max_depth, player, total_eat)
            board[position[0]][position[1]] = 0

            minEval = min(beta, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        return minEval
