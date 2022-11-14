import numpy as np
import numba as nb

from numba import njit, prange, int64, typeof
from numba.types import bool_
from numba.experimental import jitclass

from src.utils import timeit
from numba_src.numba_utils import is_capture, get_numba_sequence_frequences, is_array_equal, display
from numba_src.numba_algorithm import numba_minimax

from copy import deepcopy

@njit("int64[:,:](int64[:,:], int64[:], int64)", fastmath=True)
def add_value(arr, pos, value):
    arr[pos[0], pos[1]] = value
    return arr

@njit("UniTuple(int64[:,:], 2)(int64[:,:], int64[:,:], int64[:], int64)", fastmath=True)
def update(board, patterns, position, color):
    patterns_cnt_before = get_numba_sequence_frequences(board, position)
    stone_1, stone_2 = is_capture(board, position, color)
    if stone_1 != (-1, -1) and stone_2 != (-1, -1):
        add_value(board, np.array(stone_1, dtype=np.int64), 0)
        add_value(board, np.array(stone_2, dtype=np.int64), 0)
    add_value(board, position, color)
    patterns_cnt_after = get_numba_sequence_frequences(board, position)
    diff = np.subtract(patterns_cnt_after, patterns_cnt_before)
    updated_patterns = np.add(patterns, diff[:, :])
    return board, updated_patterns
   
@njit("int64(int64[:])", fastmath=True)
def get_score(color_patterns):
    # patterns_values = [100000, 50000, 5000, 500, 100, 10]
    patterns_values = [100000, 50000, 10000, 5000, 1000, 100, 10]
    score = 0
    for i in range(7):
        if color_patterns[i] != 0:
            score += patterns_values[i] * color_patterns[i]
    return score

# @njit("int64[:,:](ListType(int64[:]))", fastmath=True)
@njit
def make_2d(array_list):
    width = len(array_list)
    height = array_list[0].shape[0]
    array_2d = np.zeros((width, height), dtype=np.int64)
    for i in prange(width):
        array_2d[i] = array_list[i]
    return(array_2d)

@njit("int64[:,:](int64[:,:])", fastmath=True)
def remove_oob(arr):
    mask = ((arr[:, 0] >= 0) & (arr[:, 0] < 19) & (arr[:, 1] >= 0) & (arr[:, 1] < 19))
    return arr[mask, :]

@njit("int64[:,:](int64[:,:], int64[:,:])", fastmath=True)
def remove_stones(possible_pos, stones):
    mask = np.zeros(possible_pos.shape[0], dtype=bool_)
    lstones = len(stones)
    lpossible_pos = len(possible_pos)
    for i in prange(lpossible_pos):
        found = False
        for j in prange(lstones):
            if is_array_equal(stones[j], possible_pos[i]):
                mask[i] = False
                found = True
        if not found:
            mask[i] = True
    return possible_pos[mask]

@njit("int64[:,:](int64[:,:])", fastmath=True)
def remove_double(possible_pos):
    mask = np.zeros(possible_pos.shape[0], dtype=bool_)
    l = len(possible_pos)
    for i in prange(l):
        found = False
        for j in prange(l):
            if i != j and is_array_equal(possible_pos[i], possible_pos[j]):
                mask[i] = False
                mask[j] = True
                found = True
        if not found and not mask[i]:
            mask[i] = True
    return possible_pos[mask]

@njit("int64[:,:](int64[:,:])", fastmath=True)
def get_available_pos(board):
    moves = np.array(
                [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
            )
    stones = np.concatenate((np.argwhere(board == -1), np.argwhere(board == 1)), axis=0)
    possible_pos = nb.typed.List()
    for i in range(len(stones)):
        for j in range(len(moves)):
            pos = moves[j] + stones[i]
            possible_pos.append(pos)
    np_possible_pos = make_2d(possible_pos)
    np_possible_pos = remove_oob(np_possible_pos)
    np_possible_pos = remove_stones(np_possible_pos, stones)
    np_possible_pos = remove_double(np_possible_pos)
    return np_possible_pos

# @njit
def sort_moves(state, moves, n, is_maximiser):
        #add on columns to put score in it
        scored_moves = np.zeros((moves.shape[0], moves.shape[1] + 1), dtype=np.int64)
        scored_moves[:,:-1] = moves
        #for each pos evaluate new state
        for i in prange(len(moves)):
            tmp = state.next_dc(moves[i], -state.color)
            # print(tmp.color)
            # display(tmp)    
            # print("patterns:")
            # print(tmp.patterns)
            scored_moves[i, 2] = tmp.evaluate()
            # print(f"scored: {scored_moves[i]}")

        ind = np.argsort(scored_moves[:, -1])
        scored_moves = scored_moves[ind] #ascending order
        if is_maximiser:
            scored_moves = scored_moves[::-1] #descending order
        # print("scored_moves:")
        # print(scored_moves)
        scored_moves = scored_moves[:n][:, :-1] #n first move
        # print("updated scored_moves:")
        # print(scored_moves)
        return scored_moves

# @njit("int64[:,:](int64[:,:], boolean)")
# @njit
# @timeit
# def get_best_moves(state, is_maximiser):
#     moves = get_available_pos(state.board)
#     sorted_moves = sort_moves(state, moves, 10, is_maximiser)
#     return sorted_moves

@timeit
def get_best_move(state, depth, is_maximiser):
    best_moves = state.get_best_moves(is_maximiser)
    # print(best_moves)
    best_score = np.iinfo(np.int32).min if is_maximiser else np.iinfo(np.int32).max
    for i in range(len(best_moves)):
        score = numba_minimax(
            state.next_dc(best_moves[i], -state.color),
            np.iinfo(np.int32).min,
            np.iinfo(np.int32).max,
            depth - 1,
            not is_maximiser,
        )
        # state.prev()
        if (is_maximiser and score > best_score) or (
            not is_maximiser and score < best_score
        ):
            best_score = score
            best_move = best_moves[i]
    return best_move, best_score


@njit("int64[:,:](int64, optional(int64[:,:]))")
def init_board(size, board):
    if board is not None:
        return np.copy(board)
    return np.zeros((size, size), dtype=np.int64)

@njit("int64[:,:](optional(int64[:,:]))")
def init_patterns(patterns):
    if patterns is not None:
        return np.copy(patterns)
    init_patterns = np.zeros((3, 7), dtype=np.int64)
    # init_patterns[2] = [100000, 50000, 5000, 500, 100, 10]
    init_patterns[2] = [100000, 50000, 10000, 5000, 1000, 100, 5]
    return init_patterns

@njit("int64[:](optional(int64[:]))")
def init_last_move(last_move):
    if last_move is not None:
        return np.copy(last_move)
    return np.zeros((2), dtype=np.int64)

spec = [
    ("size", int64),
    ("color", int64),
    ("board", int64[:,:]),
    ("patterns", int64[:,:]),
    ("last_move", int64[:]),
]

# @jitclass(spec=spec)
class GameState:
    def __init__(self, size=19, color=-1, board=None, patterns=None, last_move=None) -> None:
        self.size = size
        self.color = color
        self.board = self._board(board)
        self.patterns = self._patterns(patterns)
        self.last_move = self._last_move(last_move)

    def _board(self, board):
        return init_board(self.size, board)

    def _patterns(self, patterns):
        return init_patterns(patterns)

    def _last_move(self, last_move):
        return init_last_move(last_move)

    def __hash__(self) -> int:
        pass

    def is_finished(self):
        return False

    # @timeit
    def next(self, position):
        new_state = GameState(
            size=19,
            color=-self.color,
            board=self.board,
            patterns=self.patterns,
            last_move=position
        )
        new_state.board, new_state.patterns = update(self.board, self.patterns, position, -self.color)
        return new_state


    def next_dc(self, position, color):
        new_state = GameState(
            size=19,
            color=color,
            board=self.board.copy(),
            patterns=self.patterns.copy(),
            last_move=position
        )
        new_state.board, new_state.patterns = update(new_state.board, new_state.patterns, position, color)
        return new_state

    def get_best_moves(self, is_maximiser):
        moves = get_available_pos(self.board)
        sorted_moves = sort_moves(self, moves, 5, is_maximiser)
        return sorted_moves


    # @timeit
    def evaluate(self):
        black_score = get_score(self.patterns[0])
        white_score = get_score(self.patterns[1])
        # print(f"BLACK SCORE: {black_score}")
        # print(f"WHITE SCORE: {white_score}")
        if self.color == -1:
            return black_score
        return white_score
        # return white_score + black_score

    def print_color(self):
        if self.color == -1:
            print("BLACK")
        else:
            print("WHITE")