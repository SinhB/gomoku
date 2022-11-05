# #!python
# #cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np

ctypedef np.int_t DTYPE_t

def get_available_positions(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef np.ndarray[np.int_t, ndim=2] moves
    cdef np.ndarray[np.int_t, ndim=2] possible_moves
    cdef np.ndarray[np.uint8_t, ndim=1, cast=True] in_board

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
    return possible_pos[:10,:]

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

@cython.boundscheck(False)
@cython.wraparound(False)
def _get_diag(np.ndarray[np.int_t, ndim=2] b, int size, d_list=[]):
    cdef int i

    for i in range(-size + 1, size - 1):
        d_list.append(np.diag(b, k=i))
    return d_list

@cython.boundscheck(False)
@cython.wraparound(False)
def get_diagonals(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef l
    cdef np.ndarray[np.int_t, ndim=2] diagonals
    # cdef np.ndarray[np.int_t, ndim=1] diag_list

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


def get_rows(np.ndarray[np.int_t, ndim=2] board, int size):
    cdef int i
    cdef np.ndarray[np.int_t, ndim=2] rows

    rows = board[~np.all(board == 0, axis=1)]
    b = np.full((rows.shape[0], 1), 3)

    rows = np.concatenate((rows, b), axis=1)

    return np.concatenate(rows)

def get_new_threats(np.ndarray[np.int_t, ndim=2] board, np.ndarray[np.int_t, ndim=1] position):
    # print("check_rules")
    # print(board)
    # print(board[position[0]][position[1]])
    print(type(position))
    b = board[position[0]-3:position[0]+4, position[1]-3:position[1]+4]
    # print(b)
    b[3][3] = 9
    # print(b)

    diags = get_position_diagonals(b, 9)
    rows = get_position_rows(b, 9)
    columns = get_position_columns(b, 9)

    # print(f"Diag : \n{diags}\n")
    # print(f"rows : \n{rows}\n")
    # print(f"columns : \n{columns}\n")

    # [0, 0, 0, 9, 1, 1, 0] = open three
    # [0, 0, 0, 9, 0, 1, 1] = ?
    open_three = 0
    for diag in diags:
        left = diag[0:3]
        right = diag[4:7]
        # print(left)
        # print(right)
        if (left == 1).sum() >= 2 or (right == 1).sum() >= 2:
            open_three += 1
        # print((left == 1).sum())
        # print((right == 1).sum())
    
    for row in rows:
        left = row[0:3]
        right = row[4:7]
        if (left == 1).sum() >= 2 or (right == 1).sum() >= 2:
            open_three += 1

    for col in columns:
        left = col[0:3]
        right = col[4:7]
        if (left == 1).sum() >= 2 or (right == 1).sum() >= 2:
            open_three += 1

    # print(f"open_three : {open_three}")

    if open_three >= 2:
        pass
        # print("Double three")

def check_eat(np.ndarray[np.int_t, ndim=2] board, color, np.ndarray[np.int_t, ndim=1] position):
    b = board[position[0]-3:position[0]+4, position[1]-3:position[1]+4]
    b[3][3] = 9
    print(b)

    diags = get_position_diagonals(b, 9)
    rows = get_position_rows(b, 9)
    columns = get_position_columns(b, 9)

    for row in rows:
        left = row[0:3]
        right = row[4:7]
        print(f"{left} : left.tolist() == [1, 2, 2] = {left.tolist() == [1, 2, 2]}")
        print(f"{right} : right.tolist() == [1, 2, 2] = {right.tolist() == [2, 2, 1]}")
        if (left.tolist() == [-1, 1, 1] or right.tolist() == [1, 1, -1]):
            print("EATING PAWNS")

def get_position_diagonals(b, exclude):
    fltr = [exclude]
    diags = [b[::-1, :].diagonal(i) for i in range(-b.shape[0] + 1, b.shape[1])]
    # upper-left-to-lower-right
    diags.extend(b.diagonal(i) for i in range(b.shape[1] - 1, -b.shape[0], -1))
    # remove only zeros diagonals
    diags = [d for d in diags if np.any(exclude in d)]
    # Make an 2d array from padding diagonals with "3"
    # (can't interfer with sequence search)
    max_d_length = max(len(d) for d in diags)
    diags = np.array(
        [np.pad(d, (0, max_d_length - len(d)), constant_values=3) for d in diags]
    )
    return diags

def get_position_rows(np.ndarray[np.int_t, ndim=2] b, exclude):
    # remove only zeros rows
    rows = b[~np.all(b == 0, axis=1)]
    return [r for r in rows if np.any(exclude in r)]

def get_position_columns(np.ndarray[np.int_t, ndim=2] b, exclude):
    columns = b.T
    # remove only zeros columns
    columns = columns[~np.all(columns == 0, axis=1)]
    return [c for c in columns if np.any(exclude in c)]