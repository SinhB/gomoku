"""Run a Gomoku Ninuki game
    BLACK_VALUE = -1
    WHITE_VALUE = 1
"""

import sys
import numpy as np
import timeit, functools

from src.board import BoardState
from src.gamestate import GameState, get_numpy_available_pos, get_numba_available_pos, get_best_move, next
from src.numba_utils import display
from src.heuristic import get_diagonals, numba_search_sequence, remove_blank_line
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

def print_state_attr(state):
    print(f"size: {state.size}")
    print(f"color: {state.color}")
    print(f"board:")
    display(state)
    print(f"seqs: {state.sequence_frequences}")
    print(f"last_move: {state.last_move}")

if __name__ =="__main__":
    board = BoardState(Color.BLACK, size=19)

    state = GameState()
    state.print_color()
    print_state_attr(state)
    # state.evaluate()
    
    # print(f"moves: {state.prev_moves}")

    pos = np.array([0, 1], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)
    m, s = get_best_move(state, 5, True)
    print(m, s)

    pos = np.array([3, 3], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    pos = np.array([4, 6], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    pos = np.array([5, 5], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    pos = np.array([3, 2], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    pos = np.array([4, 2], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    pos = np.array([1, 2], dtype=np.int64)
    state = next(state, pos)
    state.print_color()
    print_state_attr(state)

    m, s = get_best_move(state, 5, True)
    print(m, s)

    # # poses = state.get_available_pos()
    # np_poses = get_numpy_available_pos(state.board)
    # # print(np_poses, len(np_poses))
    # nb_poses = get_numba_available_pos(state.board)
    # print("First numba call")
    # nb_poses = get_numba_available_pos(state.board)
    # # print(nb_poses, len(nb_poses))

    # print("First call")
    # nb_poses = state.get_available_pos()
    # # print(nb_poses, len(nb_poses))


    # print(f"Available pos numpy: {timeit.timeit(functools.partial(get_numpy_available_pos, state.board), number=10000)}")
    # print(f"Available pos numba: {timeit.timeit(functools.partial(get_numba_available_pos, state.board), number=10000)}")
    # print(f"Available pos class numba: {timeit.timeit(functools.partial(state.get_available_pos), number=10000)}")


    # pos = np.array([5, 5], dtype=np.int64)
    # print(f"Next class numpy: {timeit.timeit(functools.partial(board.next, pos), number=10000)}")
    # print(f"Next class numba: {timeit.timeit(functools.partial(state.next, pos), number=10000)}")






    # board = board.next([3, 4])
    # board = board.next([4, 5])
    # board = board.next([5, 8])
    # board = board.next([6, 9])
    # board = board.next([2, 7])
    # board = board.next([3, 7])
    # board = board.next([3, 5])
    # board = board.next([0, 8])
    # print(board.color)
    # board.is_legal_move([10,10])
    # board = board.next([10,10])
    # board.display()
    # print(f"COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos= board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # print(board.color)
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"AGAIN NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()
    # print(board.color)
    # print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    # pos = board.get_best_move(4, True)
    # print(pos)
    # print(pos[2])
    # board = board.next(pos[0])
    # board.display()

    # print(f"Signature after call remove", remove_blank_line.nopython_signatures)
    # print(f"Signature after call numba search", numba_search_sequence.nopython_signatures)

    sys.exit()