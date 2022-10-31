import numpy as np
from numba import njit, types

from src.heuristic import get_numba_sequence_frequences
from src.utils import timeit


# @timeit
def minimax(state, alpha, beta, depth, is_maximiser):
    if depth == 0 or state.is_finished():
        return evaluate_state(state._board, state.color.swap().name)

    if is_maximiser:
        best_eval = -9999
        for sorted_move in state.get_best_moves(is_maximiser):
            move = sorted_move[1]
            evaluation = minimax(state.next(move), alpha, beta, depth - 1, False)
            best_eval = max(best_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            return best_eval
    else:
        best_eval = 9999
        for sorted_move in state.get_best_moves(not is_maximiser):
            move = sorted_move[1]
            evaluation = minimax(state.next(move), alpha, beta, depth - 1, True)
            best_eval = min(best_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            return best_eval

@njit
def evaluate_state(board, color):
    # print(f"COLOR in EVALUATE: {color}")
    # print(f"SELF.COLOR in EVALUATE: {state.color}")
    current_threats = get_numba_sequence_frequences(board)
    priority_keys = (
        "five",
        "open_four",
        "simple_four",
        "open_three",
        "broken_three",
        "simple_three",
        "open_two",
        "broken_two",
        "simple_two",
    )

    counter = 2
    score = 0
    for i, key in enumerate(priority_keys):
        # print(f"IN LOOP: for {key} {current_threats[color][key]}")
        if counter == 0:
            return score
        if current_threats[color][key] != 0:
            counter -= 1
            score += 9 - i * current_threats[color][key]
    return score
