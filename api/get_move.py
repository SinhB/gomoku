import numpy as np
import random
import time

import board_utils
import board_functions
from get_threats import get_new_threats

def get_next_move(board, depth, maximizing_player, player, total_eat, empty_board, cutoff, quick_play, timer_start):
    alpha = np.iinfo(np.int64).min
    beta = np.iinfo(np.int64).max
    if empty_board:
        coord = (random.randint(6, 12), random.randint(6, 12))
        return np.array((coord), dtype=np.int64)
    else:
        moves_results = minimax(board, depth, alpha, beta, maximizing_player, 0, depth, player, total_eat, False, cutoff, quick_play, timer_start)
        moves_results.sort(key=lambda tup: tup[0], reverse=True)
        best_score = moves_results[0][0]
        best_scores = list(filter(lambda tup: tup[0] == best_score, moves_results))
        random.shuffle(best_scores)
        return best_scores[0][1]

def get_positions(board, maximizing_player, player, total_eat, depth, cutoff, quick_play):
    available_pos = board_utils.get_available_pos(board)

    eval_to_pos = [get_new_threats(board, p, maximizing_player, player, total_eat[player], total_eat[player * -1], depth) for p in available_pos]

    # Remove is forbidden
    eval_to_pos = list(filter(lambda tup: tup[4] == False, eval_to_pos))

    eval_to_pos.sort(key=lambda tup: tup[1], reverse=maximizing_player)

    if cutoff > 0 and not maximizing_player:
        cutoff_value = eval_to_pos[0][1] * cutoff
        eval_to_pos = list(filter(lambda tup: tup[1] <= cutoff_value, eval_to_pos))

    if depth > 4:
        if quick_play:
            return eval_to_pos[:min(2, len(eval_to_pos))]
        else:
            return eval_to_pos[:min(4, len(eval_to_pos))]
    return eval_to_pos

def minimax(board, depth, alpha, beta, maximizing_player, score, max_depth, player, total_eat, is_win, cutoff, quick_play, timer_start):
    if depth == 0 or is_win or quick_play and time.time() - timer_start > 0.49 and max_depth - depth > 1:
        return score

    best_position = get_positions(board, maximizing_player, player, total_eat, max_depth - depth + 1, cutoff, quick_play)

    if depth == max_depth:
        moves_results = []

    if maximizing_player:
        maxEval = np.iinfo(np.int32).min
        for position, new_score, captured_stones, is_win, _, new_eat in best_position:
            board = board_functions.add_stone(board, player, position, captured_stones)

            total_eat[player] += new_eat
            evaluation = minimax(board, depth - 1, alpha, beta, False, score + new_score, max_depth, player, total_eat, is_win, cutoff, quick_play, timer_start)
            total_eat[player] -= new_eat

            board = board_functions.remove_stone(board, player, position, captured_stones)
            if depth == max_depth:
                moves_results.append((evaluation, position))

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        if depth == max_depth:
            return moves_results
        return maxEval

    else:
        minEval = np.iinfo(np.int32).max
        for position, new_score, captured_stones, is_win, _, new_eat in best_position:
            board = board_functions.add_stone(board, -player, position, captured_stones)

            total_eat[-player] += new_eat
            evaluation = minimax(board, depth - 1, alpha, beta, True, score + new_score, max_depth, player, total_eat, is_win, cutoff, quick_play, timer_start)
            total_eat[-player] -= new_eat

            board = board_functions.remove_stone(board, -player, position, captured_stones)

            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)
            if beta <= alpha:
                break

        return minEval