#!python
#cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np

import get_lines
import get_threats

ctypedef np.int_t DTYPE_t
@cython.boundscheck(False)
@cython.wraparound(False)
def get_next_move(
    np.ndarray[np.int_t, ndim=2] board,
    int size,
    int depth
):

    cdef int alpha
    cdef int beta
    cdef bint maximizing_player

    alpha = -100000000
    beta = 100000000
    maximizing_player = True
    available_pos = get_lines.get_available_positions(board, size)
    # good_pos = sort_moves(available_pos, maximizing_player, 10)
    best_position = available_pos[0]
    score = -100000000


    diags = get_lines.get_diagonals(board, size)
    rows = get_lines.get_rows(board, size)
    columns = get_lines.get_rows(board.T, size)
    current_threats = get_threats.get_sequences(diags, rows, columns)

    best_position = filter_pos(board, available_pos, maximizing_player)
    for position, new_threats in best_position:
        print(position)

        board[position[0]][position[1]] = 1

        next_move = minimax(board, depth, alpha, beta, maximizing_player, size, new_threats)
        print("Next move:")
        print(next_move)
        board[position[0]][position[1]] = 0
    return 5

def evaluate(current_threats, str color):
    # print("Evaluate")
    # print(current_threats)

    priority_keys = (
        "five",
        "open_four",
        "simple_four",
        "open_three",
        "broken_three",
        "simple_three",
        "open_two",
        "broken_two",
        "simple_two",
    )

    # Get the first 'counter' type of sequence to make the score
    counter = 2
    score = 0
    for i, key in enumerate(priority_keys):
        if counter == 0:
            return score
        if current_threats[color][key] != 0:
            counter -= 1
            score += 9 - i * current_threats[color][key]
    return score

def filter_pos(np.ndarray[np.int_t, ndim=2] board, available_pos, maximizing_player):
    eval_to_pos = []
    for position in available_pos:
        if maximizing_player:
            board[position[0]][position[1]] = 1
        else:
            board[position[0]][position[1]] = -1
        new_threats = get_threats.get_new_threats(board, position[0], position[1])
        board[position[0]][position[1]] = 0

        if not maximizing_player:
            eval_to_pos.append((evaluate(new_threats, "WHITE"), (position, new_threats)))
        else:
            eval_to_pos.append((evaluate(new_threats, "BLACK"), (position, new_threats)))

    if maximizing_player:
        eval_to_pos.sort(key=lambda tup: tup[0])
    else:
        eval_to_pos.sort(key=lambda tup: tup[0], reverse=True)
    new_list = []
    for i in range(0, 5):
        new_list.append(eval_to_pos[i][1])
    return new_list

def minimax(
    np.ndarray[np.int_t, ndim=2] board,
    int depth,
    int alpha,
    int beta,
    bint maximizing_player,
    int size,
    current_threats
):
    # if depth == 0 or is_finished():
    if depth == 0:
        # return evaluate(board, size, current_threats, "WHITE")
        x = evaluate(current_threats, "BLACK")
        # x = evaluate(current_threats, "BLACK")
        # print(x)
        return x
    available_pos = get_lines.get_available_positions(board, size)
    best_position = filter_pos(board, available_pos, maximizing_player)
    if maximizing_player:
        maxEval = -10000000
        # for position in best_position:
        for position, new_threats in best_position:
            board[position[0]][position[1]] = 1

            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            board[position[0]][position[1]] = 0

            maxEval = max(alpha, eval)
            alpha = max(alpha, eval)
            # print(f"alpha : {alpha}")
            if beta <= alpha:
                # print("BREAK")
                break
        return maxEval
    else:
        minEval = 10000000
        # for position in best_position:
        for position, new_threats in best_position:
            board[position[0]][position[1]] = -1
            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            board[position[0]][position[1]] = 0

            minEval - min(beta, eval)
            beta = min(beta, eval)
            # print(f"beta : {beta}")
            if beta <= alpha:
                # print("BREAK")
                break
        return minEval

