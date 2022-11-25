import random

import get_lines
import board_functions
from get_threats import get_new_threats 

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
    alpha = -2_000_000_000
    beta = 2_000_000_000
    moves_results = minimax(board, depth, alpha, beta, maximizing_player, size, 0, depth, player, total_eat)
    moves_results.sort(key=lambda tup: tup[0], reverse=True)
    print(moves_results)
    return moves_results[0][1]

def get_positions(board, maximizing_player, player, size, total_eat):
    eval_to_pos = []
    # import time

    # start = time.time()
    available_pos = get_lines.get_available_positions(board, size)
    # print(f"Get moves : {time.time() - start}")

    if len(available_pos) == 0:
        return [([random.randint(6, 12), random.randint(6, 12)], 1)]
    
    # start = time.time()
    eval_to_pos = [(p, get_new_threats(board, p, maximizing_player, player, total_eat)) for p in available_pos]
    # print(f"Eval to p : {time.time() - start}")

    eval_to_pos.sort(key=lambda tup: tup[1], reverse=maximizing_player)

    return eval_to_pos[:10]

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats, max_depth, player, total_eat):
    if depth == 0 or current_threats >= 50_000_000 or current_threats <= -50_000_000:
        return current_threats

    best_position = get_positions(board, maximizing_player, player, size, total_eat)

    if depth == max_depth:
        moves_results = []

    if maximizing_player:
        maxEval = -2_000_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = player

            evaluation = minimax(board, depth - 1, alpha, beta, False, size, new_threats, max_depth, player, total_eat)
            board[position[0]][position[1]] = 0

            if depth == max_depth:
                moves_results.append((evaluation, position))

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                # print(f"{bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        if depth == max_depth:
            return moves_results
        return maxEval

    else:
        minEval = 2_000_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = player * -1

            evaluation = minimax(board, depth - 1, alpha, beta, True, size, new_threats, max_depth, player, total_eat)
            board[position[0]][position[1]] = 0

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break

        return minEval
