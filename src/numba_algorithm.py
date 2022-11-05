import numpy as np
from numba import njit


# @njit
def numba_minimax(state, alpha, beta, depth, is_maximiser):
    if depth == 0 or state.is_finished():
        return state.evaluate()

    if is_maximiser:
        best_eval = np.iinfo(np.int32).min #-9999
        for move in state.get_best_moves(is_maximiser):
            evaluation = numba_minimax(state.next(move), alpha, beta, depth - 1, False)
            best_eval = max(best_eval, evaluation)
            alpha = max(alpha, evaluation)
            state.prev()
            if beta <= alpha:
                break
        return best_eval
    else:
        best_eval = np.iinfo(np.int32).max #9999
        for move in state.get_best_moves(not is_maximiser):
            evaluation = numba_minimax(state.next(move), alpha, beta, depth - 1, True)
            best_eval = min(best_eval, evaluation)
            beta = min(beta, evaluation)
            state.prev()
            if beta <= alpha:
                break
        return best_eval