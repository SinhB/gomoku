from numba import njit, prange
from functools import cache

from src.heuristic import get_numba_sequence_frequences
from src.utils import timeit

@cache
def minimax(state, alpha, beta, depth, is_maximiser, counter):
    if depth == 0 or state.is_finished():
        return evaluate_state(state._board, state.color.swap().name), counter

    if is_maximiser:
        best_eval = -9999
        for sorted_move in state.get_best_moves(is_maximiser):
            move = sorted_move[1]
            evaluation, counter = minimax(state.next(move), alpha, beta, depth - 1, False, counter + 1)
            best_eval = max(best_eval, evaluation)
            alpha = max(alpha, evaluation)
            state.delete_last_stone()
            if beta <= alpha:
                break
        return best_eval, counter
    else:
        best_eval = 9999
        for sorted_move in state.get_best_moves(not is_maximiser):
            move = sorted_move[1]
            evaluation, counter = minimax(state.next(move), alpha, beta, depth - 1, True, counter + 1)
            best_eval = min(best_eval, evaluation)
            beta = min(beta, evaluation)
            state.delete_last_stone()
            if beta <= alpha:
                break
        return best_eval, counter


# @njit(fastmath=True)
def evaluate_state(board, color):
    """
        "five",
        "open_four",
        "simple_four",
        "open_three",
        "broken_three",
        "simple_three",
        "open_two",
        "broken_two",
        "simple_two",
    """
    current_threats = get_numba_sequence_frequences(board)

    # Get the first 'counter' type of sequence to make the score
    counter = 2
    score = 0

    # print(current_threats)

    if color == "BLACK":
        seq_index = 0
    elif color == "WHITE":
        seq_index = 1

    for i in prange(9):
        # print(f"in loop, i: {i}, value: {current_threats[seq_index, i]}")
        if counter == 0:
            return score
        if current_threats[seq_index, i] != 0:
            counter -= 1
            score += (1,5 * pow(1.8, ((9 - i) * (int(current_threats[seq_index, i])))))[1] #+ current_threats[2, i])
    return score
