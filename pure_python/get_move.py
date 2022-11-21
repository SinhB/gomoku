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

def get_next_move(board, size, depth, maximizing_player):
    alpha = -1_000_000_000
    beta = 1_000_000_000
    moves_results = minimax(board, depth, alpha, beta, maximizing_player, size, 0, depth)
    print(moves_results)
    moves_results.sort(key=lambda tup: tup[0])
    return moves_results[0][1]

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
    # for i in range(0, len(eval_to_pos)):
    for i in range(0, min(5, len(eval_to_pos))):
        new_list.append(eval_to_pos[i][1])

    return new_list

def minimax(board, depth, alpha, beta, maximizing_player, size, current_threats, max_depth):
    # print(current_threats)
    # if depth == 0 or is_finished():
    # print(f"current_threats : {current_threats} {depth}")
    if depth == 0 or current_threats >= 100_000_000 or current_threats <= -100_000_000:
        return current_threats
    available_pos = get_lines.get_available_positions(board, size)
    best_position = filter_pos(board, available_pos, maximizing_player)

    if depth == max_depth:
        moves_results = []

    if maximizing_player:
        maxEval = -100_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = 1

            evaluation = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, 0 + new_threats, max_depth)
            if depth == max_depth:
                moves_results.append((evaluation, position))
            board[position[0]][position[1]] = 0

            maxEval = max(alpha, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                # print(f"{bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        if depth == max_depth:
            return moves_results
        return maxEval

    else:
        minEval = 100_000_000
        for position, new_threats in best_position:
            board[position[0]][position[1]] = -1

            evaluation = minimax(board, depth - 1, alpha, beta, not maximizing_player, size, 0 + new_threats, max_depth)
            if depth == max_depth:
                moves_results.append((evaluation, position))
            board[position[0]][position[1]] = 0

            minEval = min(beta, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                # print(f"{bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {bcolors.ENDC}")
                break
        if depth == max_depth:
            return moves_results
        return minEval
