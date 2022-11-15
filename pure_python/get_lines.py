import numpy as np

def get_available_positions(board, size):
    all_stones = np.argwhere(board != 0)
    moves = np.array([[1, 0], [-1, 0], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 1], [-1, -1]])
    possible_pos = np.vstack(all_stones + moves[:, None])
    in_board = (
        (possible_pos[:, 0] >= 0)
        & (possible_pos[:, 0] < size)
        & (possible_pos[:, 1] >= 0)
        & (possible_pos[:, 1] < size)
    )
    possible_pos = possible_pos[in_board, :]
    possible_pos = np.unique(
        possible_pos[
            np.all(np.any((possible_pos - all_stones[:, None]), axis=2), axis=0)
        ],
        axis=0,
    )
    # return possible_pos
    return possible_pos

def remove_blank_line(array):
    # cdef np.ndarray[np.int_t, ndim=1] flatten_arr
    sumrow = np.abs(array).sum(1)
    array = array[sumrow > 0]

    # Flatten the board with 3 as separator
    Sa = array.shape
    fill = np.full((Sa[0], Sa[1] + 1), 3)
    fill[:, :-1] = array
    flatten_arr = fill.flatten()
    return flatten_arr

def _get_diag(b, size, d_list=[]):

    for i in range(-size + 1, size - 1):
        d_list.append(np.diag(b, k=i))
    return d_list

def get_diagonals(board, size):
    diag_list = _get_diag(board, size)
    # flip to get others diags
    board = np.flip(np.fliplr(board))
    diag_list = _get_diag(board, size, diag_list)

    max_len = 0
    for i in range(len(diag_list)):
        if diag_list[i].size > max_len:
            max_len = diag_list[i].size

    # Pad diag to concatenate them in one ndarray
    all_diags = np.zeros((1, max_len), dtype=np.int8)
    for diag in diag_list:
        d = np.full((1, max_len), 0, dtype=np.int8)
        d[-1, : diag.shape[0]] = diag
        all_diags = np.concatenate((all_diags, d), axis=0)

    return remove_blank_line(all_diags)


def get_rows(board, size):
    rows = board[~np.all(board == 0, axis=1)]
    b = np.full((rows.shape[0], 1), 3)

    rows = np.concatenate((rows, b), axis=1)

    return np.concatenate(rows)

def get_position_diagonals(board, column_idx, row_idx):
    lr_diag = board.diagonal(row_idx - column_idx)
    w = board.shape[1]
    rl_diag = np.fliplr(board).diagonal(w - column_idx - 1 - row_idx)
    return lr_diag, rl_diag

def get_position_rows(b, row_idx):
    return b[row_idx, :]

def get_position_columns(b, column_idx):
    return b[:, column_idx]