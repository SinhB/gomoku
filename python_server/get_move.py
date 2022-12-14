import numpy as np
import random

import get_lines
import board_functions
from get_threats import get_new_threats 
from board_functions import bcolors

def get_next_move(board, size, depth, maximizing_player, player, total_eat, empty_board):
    alpha = np.iinfo(np.int64).min
    beta = np.iinfo(np.int64).max
    if empty_board:
        coord = (random.randint(6, 12), random.randint(6, 12))
        return np.array((coord), dtype=np.int64)
    else:
        moves_results = minimax(board, depth, alpha, beta, maximizing_player, size, 0, depth, player, total_eat)
        moves_results.sort(key=lambda tup: tup[0], reverse=True)
        return moves_results[0][1]

def get_positions(board, maximizing_player, player, size, total_eat, depth):
    available_pos = get_lines.get_available_pos(board)

    eval_to_pos = [(p, get_new_threats(board, p, maximizing_player, player, total_eat[player], total_eat[player * -1], depth)) for p in available_pos]

    eval_to_pos.sort(key=lambda tup: tup[1][0], reverse=maximizing_player)


    cutoff = eval_to_pos[0][1][0] * 0.8
    if maximizing_player:
        eval_to_pos = list(filter(lambda tup: tup[1][0] >= cutoff, eval_to_pos))
    else:
        eval_to_pos = list(filter(lambda tup: tup[1][0] <= cutoff, eval_to_pos))

    return eval_to_pos
    # return eval_to_pos[:min(4, len(eval_to_pos))]

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats, max_depth, player, total_eat):
    # print(depth)
    if depth == 0 or current_threats >= 100_000 or current_threats <= -100_000:
        return current_threats

    best_position = get_positions(board, maximizing_player, player, size, total_eat, max_depth - depth + 1)

    if depth == max_depth:
        moves_results = []

    if maximizing_player:
        maxEval = np.iinfo(np.int32).min
        for position, new_threats in best_position:
            board = board_functions.add_stone(board, player, position, new_threats[1])
            evaluation = minimax(board, depth - 1, alpha, beta, False, size, current_threats + new_threats[0], max_depth, player, total_eat)
            board = board_functions.remove_stone(board, player, position, new_threats[1])
            
            if depth == max_depth:
                moves_results.append((evaluation, position))

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            # if beta <= alpha or evaluation >= 50_000_000:
            if beta <= alpha:
                # print(f"{bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        if depth == max_depth:
            return moves_results
        return maxEval

    else:
        minEval = np.iinfo(np.int32).max
        for position, new_threats in best_position:
            board = board_functions.add_stone(board, -player, position, new_threats[1])

            evaluation = minimax(board, depth - 1, alpha, beta, True, size, current_threats + new_threats[0], max_depth, player, total_eat)

            board = board_functions.remove_stone(board, -player, position, new_threats[1])

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            # if beta <= alpha or evaluation <= -50_000_000:
            if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break

        return minEval
