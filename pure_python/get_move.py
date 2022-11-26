import random

import get_lines
import board_functions
from get_threats import get_new_threats 
from board_functions import bcolors

def get_next_move(board, size, depth, maximizing_player, player, total_eat, empty_board):
    alpha = -2_000_000_000
    beta = 2_000_000_000
    if empty_board:
        return [random.randint(6, 12), random.randint(6, 12)]
    else:
        moves_results = minimax(board, depth, alpha, beta, maximizing_player, size, 0, depth, player, total_eat)
        moves_results.sort(key=lambda tup: tup[0], reverse=True)
        print(moves_results)
        return moves_results[0][1]

def get_positions(board, maximizing_player, player, size, total_eat):
    # print(f"pre sort : {eval_to_pos}")
    available_pos = get_lines.get_available_pos(board)
    # print(f"ave pos  : {[x for x in available_pos]}")

    eval_to_pos = [(p, get_new_threats(board, p, maximizing_player, player, total_eat[player], total_eat[player * -1])) for p in available_pos]
    # print(eval_to_pos)
    # input()

    # print(f"non sort : {[x[0] for x in eval_to_pos]}\n")
    eval_to_pos.sort(key=lambda tup: tup[1], reverse=maximizing_player)

    # print(f"sorted   : {[x[0] for x in eval_to_pos]}\n")

    cutoff = eval_to_pos[0][1] * 0.8
    if maximizing_player:
        eval_to_pos = list(filter(lambda tup: tup[1] >= cutoff, eval_to_pos))
    else:
        eval_to_pos = list(filter(lambda tup: tup[1] <= cutoff, eval_to_pos))
    # print(f"Filtered : {[x[0] for x in eval_to_pos]}\n\n\n")
    # return eval_to_pos
    return eval_to_pos[:min(5, len(eval_to_pos))]

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats, max_depth, player, total_eat):
    if depth == 0 or current_threats >= 50_000_000 or current_threats <= -50_000_000:
        return current_threats

    best_position = get_positions(board, maximizing_player, player, size, total_eat)

    if depth == max_depth:
        # print(best_position)
        # input()
        moves_results = []

    if maximizing_player:
        maxEval = -2_000_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = player

            evaluation = minimax(board, depth - 1, alpha, beta, False, size, new_threats, max_depth, player, total_eat)
            # evaluation = minimax(board, depth - 1, alpha, beta, False, size, current_threats + new_threats, max_depth, player, total_eat)
            board[position[0]][position[1]] = 0

            if depth == max_depth:
                moves_results.append((evaluation, position))

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha or evaluation >= 50_000_000:
            # if beta <= alpha:
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
            # evaluation = minimax(board, depth - 1, alpha, beta, True, size, current_threats - new_threats, max_depth, player, total_eat)
            board[position[0]][position[1]] = 0

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha or evaluation <= -50_000_000:
            # if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break

        return minEval
