import board_utils
import numba as nb
import numpy as np
from numba import njit

@njit("UniTuple(boolean, 4)(int64[:], int64)")
def check_vulnerability(side, player):
    is_consec = True
    consec = 0

    for i in range(0, min(len(side), 2)):
        if side[i] == 0:
            if i == 0:
                return False, True, False, False
            if i == 1 and consec == 1:
                return False, False, False, True
            else:
                is_consec = False
        if side[i] == player:
            if is_consec:
                consec += 1
        if side[i] == -player:
            if i == 0:
                return True, False, False, False
            if i == 1 and consec == 1:
                return False, False, True, False
            else:
                is_consec = False
    return False, False, False, False

@njit("int64[:](boolean, int64, int64, int64, int64)")
def get_pos(is_left, index, row_index, col_index, line_type):
    """
        0: LR
        1: RL
        2: ROW
        3: COL
        return: (row, col)
    """
    if is_left:
        if line_type == 0:
            return np.array((row_index - index, col_index - index))
        if line_type == 1:
            return np.array((row_index - index, col_index + index))
        if line_type == 2:
            return np.array((row_index, col_index - index))
        if line_type == 3:
            return np.array((row_index - index, col_index))
    else:
        if line_type == 0:
            return np.array((row_index + index, col_index + index))
        if line_type == 1:
            return np.array((row_index + index, col_index - index))
        if line_type == 2:
            return np.array((row_index, col_index + index))
        if line_type == 3:
            return np.array((row_index + index, col_index))
    return np.zeros(2, dtype=np.int64)


@njit("Tuple((boolean, boolean, int64))(int64[:], int64, int64)", fastmath=True)
def check_line_breakable(line, starting_index, player):
    """Return: (is_breakable, is_left)"""
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]

    l_starting_op, l_starting_blank, l_ending_op, l_ending_blank = check_vulnerability(left, player)
    r_starting_op, r_starting_blank, r_ending_op, r_ending_blank = check_vulnerability(right, player)

    #right
    if l_starting_op and r_ending_blank:
        return True, False, 2
    if r_starting_blank and l_ending_op:
        return True, False, 1
    #left
    if r_starting_op and l_ending_blank:
        return True, True, 2
    if l_starting_blank and r_ending_op:
        return True, True, 1

    return False, False, 0


@njit("Tuple((boolean, int64[:]))(int64[:,:], int64[:], int64)", fastmath=True)
def pos_is_breakable(board, position, player):
    row_index, col_index = position
    lr_diags, rl_diags, row, column = board_utils.get_vectors(board, row_index, col_index)

    lr_starting_index = col_index if row_index > col_index else row_index
    rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index

    is_breakable, is_left, index = check_line_breakable(lr_diags, lr_starting_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 0)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(rl_diags, rl_starting_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 1)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(row, col_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 2)
        return True, pos
    is_breakable, is_left, index = check_line_breakable(column, row_index, player)
    if is_breakable:
        pos = get_pos(is_left, index, row_index, col_index, 3)
        return True, pos
    return False, np.zeros(2, dtype=np.int64)


@njit("Tuple((boolean, int64[:]))(int64[:,:], int64, int64[:], int64, int64, int64, int64)", fastmath=True)
def check_if_breakable(board, line_type, line, starting_index, player, row_index, col_index):
    left = line[0:starting_index][::-1]
    right = line[starting_index+1:]
    pos_list = [np.array((row_index, col_index))]
    for i in range(0, min(len(left), 6)):
        if left[i] == player:
            new_pos = get_pos(True, i + 1, row_index, col_index, line_type)
            pos_list.append(new_pos)
        else:
            break
    for i in range(0, min(len(right), 6)):
        if right[i] == player:
            new_pos = get_pos(False, i + 1, row_index, col_index, line_type)
            pos_list.append(new_pos)
        else:
            break
    numba_pos_list = nb.typed.List(pos_list)
    for pos in numba_pos_list:
        is_breakable, breaking_pos = pos_is_breakable(board, pos, player)
        if is_breakable:
            return True, breaking_pos
    return False, np.zeros(2, dtype=np.int64)