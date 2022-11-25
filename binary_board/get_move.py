import get_threats
import board_functions

def get_next_move(player_board, enemy_board, size, depth, maximizing_player=True):
    alpha = -1_000_000_000
    beta = 1_000_000_000

    best_position = filter_pos(player_board, enemy_board, maximizing_player)

    moves_results = []
    for position, new_threats in best_position:
        print(position)

        player_board[position] = 1
        score = minimax(player_board, enemy_board, depth, alpha, beta, not maximizing_player, size, new_threats)
        player_board[position] = 0

        if maximizing_player:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        moves_results.append((score, position))
        print(f"MOVE SCORE : {score}")
    moves_results.sort(key=lambda tup: tup[0])
    return moves_results[0][1]

def filter_pos(player_board, enemy_board, maximizing_player):
    available_pos = board_functions.get_available_positions(player_board, enemy_board)
    eval_to_pos = []
    for position in available_pos:
        new_threats = get_threats.get_new_threats(player_board, enemy_board, position, maximizing_player)

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

def minimax(player_board, enemy_board, depth, alpha, beta, maximizing_player, size, current_threats):
    # if depth == 0 or is_finished():
    # print(f"current_threats : {current_threats} {depth}")
    if depth == 0 or current_threats >= 100_000_000 or current_threats <= -100_000_000:
        return current_threats

    best_position = filter_pos(player_board, enemy_board, maximizing_player)

    if maximizing_player:
        maxEval = -100_000_000
        for position, new_threats in best_position:
            player_board[position] = 1
            evaluation = minimax(player_board, enemy_board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            player_board[position] = 0

            maxEval = max(alpha, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                # print(f"{board_functions.bcolors.OKBLUE} BREAK ALPHA : alpha = {alpha}, beta = {beta} {board_functions.bcolors.ENDC}")
                break
            # else:
            #     print(f"{board_functions.bcolors.WARNING} NO BREAK ALPHA : alpha = {alpha}, beta = {beta} {board_functions.bcolors.ENDC}")
            #     break
        return maxEval
    else:
        minEval = 100_000_000
        for position, new_threats in best_position:
            enemy_board[position] = 1
            evaluation = minimax(player_board, enemy_board, depth - 1, alpha, beta, not maximizing_player, size, new_threats)
            enemy_board[position] = 0

            minEval = min(beta, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                # print(f"{board_functions.bcolors.OKGREEN} BREAK BETA : alpha = {alpha}, beta = {beta} {board_functions.bcolors.ENDC}")
                break
            # else:
            #     print(f"{board_functions.bcolors.WARNING} NO BREAK BETA : alpha = {alpha}, beta = {beta} {board_functions.bcolors.ENDC}")
            #     break
        return minEval
