"""Run a Gomoku Ninuki game
    BLACK_VALUE = -1
    WHITE_VALUE = 1
"""

import sys
import numpy as np
import timeit, functools

from src.board import BoardState
from numba_src.numba_gamestate import GameState, get_best_move, make_2d
# from src.gamestate import GameState, get_numpy_available_pos, get_numba_available_pos, get_best_move, next
from numba_src.numba_utils import display
from src.heuristic import get_diagonals, numba_search_sequence, remove_blank_line
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

def print_state_attr(state):
    print("------------------------------")
    print(f"size: {state.size}")
    print(f"color: {state.color}")
    print(f"board:")
    display(state)
    print(f"patterns:")
    print(state.patterns)
    print(f"last_move: {state.last_move}")

if __name__ =="__main__":
    # board = BoardState(Color.BLACK, size=19)

    state = GameState()
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([9, 9], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([8, 8], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([9, 8], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([9, 7], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([7, 9], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([1, 1], dtype=np.int64)
    # pos = np.array([10, 6], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    state.evaluate()

    pos = np.array([10, 6], dtype=np.int64)
    # pos = np.array([11, 5], dtype=np.int64)
    state = state.next(pos)
    state.print_color()
    print_state_attr(state)
    score = state.evaluate()
    print(score)

    # pos = np.array([8, 9], dtype=np.int64)
    # state = state.next(pos)
    # state.print_color()
    # print_state_attr(state)
    # state.evaluate()

    # poses = get_best_moves(state, True)
    pos = get_best_move(state, 5, True)
    print(pos)
    state = state.next(pos[0])
    state.print_color()
    print_state_attr(state)

    pos = get_best_move(state, 5, True)
    print(pos)
    print_state_attr(state)
    state = state.next(pos[0])
    state.print_color()
    print_state_attr(state)

    pos = get_best_move(state, 5, True)
    print(pos)
    print_state_attr(state)
    state = state.next(pos[0])
    state.print_color()
    print_state_attr(state)

    pos = get_best_move(state, 5, True)
    print(pos)
    print_state_attr(state)
    state = state.next(pos[0])
    state.print_color()
    print_state_attr(state)

    pos = get_best_move(state, 5, True)
    print(pos)
    print_state_attr(state)
    state = state.next(pos[0])
    state.print_color()
    print_state_attr(state)

    # print(get_best_moves.inspect_types())
    # print(f"Evaluate: {timeit.timeit(functools.partial(state.evaluate), number=10000)}")
    # print(f"Next: {timeit.timeit(functools.partial(state.next, pos), number=10000)}") 
    # print(f"Best Moves: {timeit.timeit(functools.partial(get_best_moves, state, True), number=10000)}") 

    sys.exit()