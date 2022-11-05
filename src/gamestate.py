"""
    BLACK = -1 / 2 / blue
    WHITE = 1 / red
"""
import numba as nb
import numpy as np

from numba.experimental import jitclass
from numba import njit, int64, prange, typeof
from numba.types import bool_

from math import pow

from src.utils import timeit
from src.numba_utils import is_array_equal, get_numba_sequence_frequences, display
from src.numba_algorithm import numba_minimax


spec = [
    ("size", int64),
    ("color", int64),
    ("board", int64[:,:]),
    ("sequence_frequences", int64[:,:]),
    ("last_move", int64[:]),
    ("prev_moves", typeof([np.zeros(2, dtype=np.int64)]))
]

@jitclass(spec=spec)
class GameState:
    def __init__(self, size=19, color=-1, board=None, seqs=None) -> None:
        self.size = size
        self.color = color
        self.board = board if board is not None else np.zeros((size, size), dtype=np.int64)
        self.sequence_frequences = seqs if seqs is not None else np.zeros((2, 9), dtype=np.int64)
        self.prev_moves = [np.zeros(x, dtype=np.int64) for x in range(0)]

    def __hash__(self) -> int:
        return hash(str(self.color))

    def add_stone(self, position):
        return add_value(self.board, position, self.color)

    def remove_stone(self, position):
        return add_value(self.board, position, 0)

    def add_move(self, position):
        self.prev_moves.append(position)

    def remove_move(self):
        self.prev_moves = self.prev_moves[:-1]

    def is_finished(self):
        return False

    def next(self, position):
        self.color = -self.color
        self.add_stone(position)
        self.add_move(position)
        return self

    def prev(self):
        self.remove_stone(self.prev_moves[-1])
        self.remove_move()
        self.color = -self.color
        return self

    def evaluate(self):
        current_threats = get_numba_sequence_frequences(self.board)
        # print(self.prev_moves)
        # print(self.color)
        # print(current_threats)
        black_score = get_score(current_threats, 0)
        white_score = get_score(current_threats, 1)
        # print(black_score)
        # print(white_score)
        if self.color == -1:
            return int(black_score)
        return int(white_score)

    # def get_best_move(self, depth, is_maximiser):
    #     sorted_moves = self.get_best_moves(is_maximiser)
    #     best_score = -9999 if is_maximiser else 9999
    #     for i in range(len(sorted_moves)):
    #         print(sorted_moves[i])
    #         self.next(sorted_moves[i])
    #         # score = numba_minimax(
    #         #     self,
    #         #     np.iinfo(np.int32).min,
    #         #     np.iinfo(np.int32).max,
    #         #     depth - 1,
    #         #     not is_maximiser,
    #         # )
    #         score = 0
    #         self.prev()
    #         if (is_maximiser and score > best_score) or (
    #             not is_maximiser and score < best_score
    #         ):
    #             best_score = score
    #             best_move = sorted_moves[i]
    #     return best_move, best_score

    def get_best_moves(self, is_maximiser):
        available_positions = self.get_available_pos()
        # sorted_moves = sort_n_moves(self, available_positions, 10, is_maximiser)
        #remove last column with score
        # print(sorted_moves)
        # sorted_moves = sorted_moves[:, :-1]
        return available_positions
        # return sorted_moves

    # def sort_n_moves(self, moves, n, is_maximiser):
    #     #add on columns to put score in it
    #     scored_moves = np.zeros((moves.shape[0], moves.shape[1] + 1), dtype=np.int64)
    #     scored_moves[:,:-1] = moves
    #     #for each pos evaluate new state
    #     for i in range(len(moves)):
    #         self.next(moves[i])
    #         scored_moves[i, 2] = self.evaluate()
    #         self.prev()

    #     ind = np.argsort(scored_moves[:, -1])
    #     scored_moves = scored_moves[ind] #ascending order
    #     if is_maximiser:
    #         scored_moves = scored_moves[::-1] #descending order
    #     scored_moves = scored_moves[:n] #n first move
    #     return scored_moves 

    def get_black_stones(self):
        return np.argwhere(self.board == -1)

    def get_white_stones(self):
        return np.argwhere(self.board == 1)

    def get_available_pos(self):
        moves = np.array(
                [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
            )
        stones = np.concatenate((np.argwhere(self.board == -1), np.argwhere(self.board == 1)), axis=0)
        lstones = len(stones)
        lmoves = len(moves)
        possible_pos = []
        for i in range(lstones):
            for j in range(lmoves):
                pos = moves[j] + stones[i]
                possible_pos.append(pos)
        possible_pos = make_2d(possible_pos)
        possible_pos = remove_oob(possible_pos)
        possible_pos = remove_stones(possible_pos, stones)
        possible_pos = remove_double(possible_pos)
        return possible_pos

    def print_color(self):
        if self.color == -1:
            print("BLACK")
        else:
            print("WHITE")

# @njit
@timeit
def get_best_move(state, depth, is_maximiser):
    sorted_moves = state.get_best_moves(is_maximiser)
    best_move = sorted_moves[0]
    best_score = np.iinfo(np.int32).min if is_maximiser else np.iinfo(np.int32).max
    # return best_move, 1
    for i in range(len(sorted_moves)):
        score = numba_minimax(
            state.next(sorted_moves[i]),
            np.iinfo(np.int32).min,
            np.iinfo(np.int32).max,
            depth - 1,
            not is_maximiser,
        )
        state.prev()
        if (is_maximiser and score > best_score) or (
            not is_maximiser and score < best_score
        ):
            best_score = score
            best_move = sorted_moves[i]
    return best_move, best_score

# @njit(fastmath=True, parallel=True)
@njit(fastmath=True)
def sort_n_moves(state, moves, n, is_maximiser):
        #add on columns to put score in it
        scored_moves = np.zeros((moves.shape[0], moves.shape[1] + 1), dtype=np.int64)
        scored_moves[:,:-1] = moves
        #for each pos evaluate new state
        for i in prange(len(moves)):
            state.next(moves[i])
            scored_moves[i, 2] = state.evaluate()
            state.prev()

        ind = np.argsort(scored_moves[:, -1])
        scored_moves = scored_moves[ind] #ascending order
        if is_maximiser:
            scored_moves = scored_moves[::-1] #descending order
        scored_moves = scored_moves[:n] #n first move
        return scored_moves

@njit(fastmath=True)
def get_score(threats, color_index):
    counter = 2
    score = 0
    for i in prange(9):
        if counter == 0:
            return score
        if threats[color_index, i] != 0:
            counter -= 1
            # score += (1.5 * pow(1.8, ((9 - i) * (int(threats[color_index, i]))) + threats[2, i]))
            score += (1.5 * pow(1.8, ((9 - i)))) #* (int(threats[color_index, i])))))
    return score

@njit("int64[:,:](int64[:,:], int64[:], int64)", fastmath=True)
def add_value(arr, pos, value):
    arr[pos[0], pos[1]] = value
    return arr

@njit(fastmath=True)
def make_2d(array_list):
    width = len(array_list)
    height = array_list[0].shape[0]
    array_2d = np.zeros((width, height), dtype=np.int64)
    for i in prange(width):
        array_2d[i] = array_list[i]
    return(array_2d)

@njit(fastmath=True)
# @njit
def remove_oob(arr):
    mask = ((arr[:, 0] >= 0) & (arr[:, 0] < 19) & (arr[:, 1] >= 0) & (arr[:, 1] < 19))
    return arr[mask, :]

@njit(fastmath=True)
# @njit
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

@njit(fastmath=True)
# @njit
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

# @timeit
@njit(fastmath=True)
# @njit
def get_numba_available_pos(board):
    moves = np.array(
            [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
        )
    stones = np.concatenate((np.argwhere(board == -1), np.argwhere(board == 1)), axis=0)
    lstones = len(stones)
    lmoves = len(moves)
    possible_pos = []
    for i in range(lstones):
        for j in range(lmoves):
            pos = moves[j] + stones[i]
            possible_pos.append(pos)
    possible_pos = make_2d(possible_pos)
    possible_pos = remove_oob(possible_pos)
    possible_pos = remove_stones(possible_pos, stones)
    possible_pos = remove_double(possible_pos)
    return possible_pos

# @timeit
def get_numpy_available_pos(board):
    moves = np.array(
            [[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]]
        )
    all_stones = np.concatenate((np.argwhere(board == -1), np.argwhere(board == 1)), axis=0)
    possible_pos = np.vstack(all_stones + moves[:, None])
    in_board = (
        (possible_pos[:, 0] >= 0)
        & (possible_pos[:, 0] < board.shape[0])
        & (possible_pos[:, 1] >= 0)
        & (possible_pos[:, 1] < board.shape[1])
    )
    possible_pos = possible_pos[in_board, :]
    possible_pos = np.unique(
        possible_pos[
            np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
        ],
        axis=0,
    )
    return possible_pos