import numpy as np

import get_lines
import get_threats

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_next_move(board, size, depth):
    alpha = -1_000_000_000
    beta = 1_000_000_000
    maximizing_player = True
    available_pos = get_lines.get_available_positions(board, size)
    # good_pos = sort_moves(available_pos, maximizing_player, 10)
    best_position = available_pos[0]

    best_position = filter_pos(board, available_pos, maximizing_player)
    moves_results = []
    for position, new_threats in best_position:
        print(position)

        board[position[0]][position[1]] = 1

        score = minimax(board, depth, alpha, beta, maximizing_player, size, new_threats)
        moves_results.append((score, position))
        print("Next move:")
        print(score)
        board[position[0]][position[1]] = 0
    moves_results.sort(key=lambda tup: tup[0])
    return moves_results[0][1]

def evaluate(current_threats, color):
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

def filter_pos(board, available_pos, maximizing_player):
    eval_to_pos = []
    for position in available_pos:
        if maximizing_player:
            board[position[0]][position[1]] = 1
        else:
            board[position[0]][position[1]] = -1
        new_threats = get_threats.get_new_threats(board, position[0], position[1], maximizing_player)
        board[position[0]][position[1]] = 0

        if not maximizing_player:
            eval_to_pos.append((new_threats, (position, new_threats)))
        else:
            eval_to_pos.append((new_threats, (position, new_threats)))

    if maximizing_player:
        eval_to_pos.sort(key=lambda tup: tup[0])
    else:
        eval_to_pos.sort(key=lambda tup: tup[0], reverse=True)

    new_list = []
    for i in range(0, min(5, len(eval_to_pos))):
        new_list.append(eval_to_pos[i][1])
    return new_list

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats):
    # print(current_threats)
    # if depth == 0 or is_finished():
    if depth == 0 or current_threats >= 100_000_000:
        return current_threats
    available_pos = get_lines.get_available_positions(board, size)
    best_position = filter_pos(board, available_pos, maximizing_player)
    if maximizing_player:
        maxEval = -100_000_000
        # for position in best_position:
        for position, new_threats in best_position:
            board[position[0]][position[1]] = 1

            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            board[position[0]][position[1]] = 0

            maxEval = max(alpha, eval)
            alpha = max(alpha, eval)
            # print(f"alpha : {alpha}")
            if beta <= alpha:
                # print(f"{bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        return maxEval
    else:
        minEval = 100_000_000
        # for position in best_position:
        for position, new_threats in best_position:
            board[position[0]][position[1]] = -1
            eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            board[position[0]][position[1]] = 0

            minEval = min(beta, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        return minEval
