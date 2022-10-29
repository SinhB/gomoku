import numpy as np
from numba import njit
# from src.board import BoardState
from src.utils import Color, timeit

@timeit
def get_best_move(state, depth):
    """
    """
    state.update_board()
    state.display()
    board = state._board
    stones = len(board[board != 0])
    print(f"STONES NB = {stones}")
    positions = state.get_available_pos()
    print(len(positions))
    for position in positions:
        if not state.is_legal_move(position):
            continue
        # value = minimax(state.next(position), np.int8.min, np.int8.max, depth -1, not is_maximiser)
    best_move = [16, 16]
    return best_move

def minimax(state, alpha, beta, depth, is_maximiser):
    if depth == 0 or state.is_finished():
        return evaluation_state(state, state.color.swap())

    if is_maximiser:
        max_eval = np.int8.min
        for move in state.legal_moves:
            evaluation = minimax(state.next(move), alpha, beta, depth -1, not is_maximiser)
            max_eval = max(max_eval, evaluation)

