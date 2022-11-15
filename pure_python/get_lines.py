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

def get_position_diagonals(board, column_idx, row_idx):
    lr_diag = board.diagonal(row_idx - column_idx)
    w = board.shape[1]
    rl_diag = np.fliplr(board).diagonal(w - column_idx - 1 - row_idx)
    return lr_diag.tolist(), rl_diag.tolist()

def get_position_rows(b, row_idx):
    return b[row_idx, :].tolist()

def get_position_columns(b, column_idx):
    return b[:, column_idx].tolist()