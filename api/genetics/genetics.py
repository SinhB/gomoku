import numpy as np
import time
import json

import board_functions
# import get_move
import genetics_get_move
# import hard_mode_get_move
# import get_lines
import genetics_get_threats
import genetics_get_hash

def is_array_equal(arr, seq):
    for arri, seqi in zip(arr, seq):
        if arri != seqi:
            return False
    return True

def check_line_win(arr, seq):
    # Check for sequence in the flatten board
    seq_len = len(seq)
    upper_bound = len(arr) - seq_len + 1
    for i in range(upper_bound):
        
        if is_array_equal(arr[i : i + seq_len], seq):
            return True

    return False

def check_win(board, position, player, total_eat, total_enemy_eat):
    if total_eat >= 5:
        return True, None
    row_index = position[0]
    col_index = position[1]

    win_array = (player, player, player, player, player)

    lr_diags, rl_diags, rows, columns = genetics_get_threats.get_vectors(board, row_index, col_index)


    if check_line_win(lr_diags, win_array):
        lr_starting_index = col_index if row_index > col_index else row_index
        is_breakable, breaking_pos = genetics_get_threats.check_if_breakable(board, 0, lr_diags, lr_starting_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            return True, None
    if check_line_win(rl_diags, win_array):
        rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
        is_breakable, breaking_pos = genetics_get_threats.check_if_breakable(board, 1, rl_diags, rl_starting_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            return True, None
    if check_line_win(rows, win_array):
        is_breakable, breaking_pos = genetics_get_threats.check_if_breakable(board, 2, rows, col_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            return True, None
    if check_line_win(columns, win_array):
        is_breakable, breaking_pos = genetics_get_threats.check_if_breakable(board, 3, columns, row_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            return True, None
    return False, None

def get_best_move(black_multis, white_multis, display_board):
    board = board_functions.init_board(19)
    total_eat = {-1: 0, 1: 0}
    empty_board = True
    priority_move = {-1: None, 1: None}
    timers = {-1: 0, 1: 0}
    player = 1
    depth = 6
    total_move = 0

    while True:
        one_move_timer = time.time()
        if type(priority_move[player]) is np.ndarray:
            move = priority_move[player]
            priority_move[player] = None
        else:
            initial_board = np.copy(board)
            if player == 1:
                move = genetics_get_move.get_next_move(initial_board, depth, True, player, total_eat, empty_board, black_multis)
            else:
                move = genetics_get_move.get_next_move(initial_board, depth, True, player, total_eat, empty_board, white_multis)
            # if player == 1:
            #     move = genetics_get_move.get_next_move(initial_board, depth, True, player, total_eat, empty_board, black_multis)
            # else:
            #     move = hard_mode_get_move.get_next_move(initial_board, depth, True, player, total_eat, empty_board)
        one_move_timer_stop = time.time()
        timers[player] += one_move_timer_stop - one_move_timer

        empty_board = False

        board, eat, eaten_pos = board_functions.place_stone(board, move, player)

        for eaten in eaten_pos:
            board[eaten[0]][eaten[1]] = 0
        total_eat[player] += eat

        total_move += 1

        is_win, breaking_pos = check_win(board, move, player, total_eat[player], total_eat[-player])
        if breaking_pos is not None:
            print(type(breaking_pos))
            priority_move[-player] = breaking_pos
        if display_board:
            board_functions.print_board(board, move)
        if is_win:
            break
        player = -player
    # print(player)
    # print(timers)
    return player, timers, total_eat, total_move

import random

def rv(x=None):
    if x == None:
        return random.randint(-1000, 1000)
    value = 50
    # value = int(1000 / x)
    return random.randint(-value, value)

def generate_multiplicators():
    multiplicators = [
        [rv(), rv(), rv(), rv(), rv()],
        0,
        rv(),
        [
            rv(),
            rv(),
            rv(),
            rv(),
            rv(),
            rv(),
            rv(),
            rv(),
        ]
    ]
    return multiplicators

def update_weight(inital_weights, generations, number_of_childrens):
    all_multis = []
    for weights in inital_weights:
        # all_multis.append(weights)
        for i in range(0, number_of_childrens):
            new_eat_weights = []
            for weigth in weights[0]:
                new_eat_weights.append(weigth + rv(1))
            new_multis = []
            for i in range(0, len(weights[3])):
                new_multis.append(weights[3][i] + rv(1))
                # genetics_get_hash
            all_multis.append([new_eat_weights, 0, weights[2] + rv(1), new_multis])
            # all_multis.append([new_eat_weights, genetics_get_hash.get_hash(new_multis, False), weights[2] + rv(1), new_multis])
            # all_multis.append([new_eat_weights, new_multis])
    return all_multis


def evaluate(winner, timers, total_eat, total_move, player, multis):
    score = 0
    if total_move < 12:
        score -= 1000
    elif total_move < 16:
        score -= 500
    elif total_move < 20:
        score -= 200
    if total_move < 25:
        score -= 100
    # if total_move > 40:
    #     score -= 50

    player_moves = total_move / 2
    # print(winner)
    # print(scores)
    # score += scores[player] / player_moves - scores[-player] / player_moves
    score += 10_000 if winner == player else 0
    # score -= total_move
    # score -= timers[player] / total_move * 0.5
    score += total_eat[player] * 1000
    score -= total_eat[-player] * 1000

    return score


def fitness(multis, number_of_ancestors):
    count = 0

    total_results = [[0, multis[i]] for i in range(0, len(multis))]

    for i in range(0, len(multis)):
        black_multi = multis[i]
        for j in range(i, len(multis)):
            print(f"Round  : {count}")
            white_multi = multis[j]
            winner, timers, total_eat, total_move = get_best_move(black_multi, white_multi, False)
            print(f"Winner : {winner} {timers} {total_move}")
            count += 1
            total_results[i][0] += evaluate(winner, timers, total_eat, total_move, 1, black_multi)
            total_results[j][0] += evaluate(winner, timers, total_eat, total_move, -1, white_multi)

    total_results.sort(key=lambda tup: tup[0], reverse=True)


    best_weights = [x[1] for x in total_results[0:int(number_of_ancestors/2)]]
    json_black = json.dumps({"multis": best_weights}, indent=2)
    with open("black.json", "w") as outfile:
        outfile.write(json_black)

    get_best_move(total_results[0][1], total_results[1][1], True)

    return best_weights


if __name__ == "__main__":
    number_of_ancestors = 10
    generations = 10
    # with open('black.json') as f:
    #     data_black = json.load(f)
    # best_black = data_black['multis']

    # with open('white.json') as f:
    #     data_white = json.load(f)
    # best_white = data_black['multis']
    # best_black = [generate_multiplicators() for i in range(0, number_of_ancestors)]

    best_black = [generate_multiplicators() for i in range(0, number_of_ancestors)]

    # for i in range(1, generations):
    number_of_childrens = 2
    i = 0
    while True:
        print(f"Generation {i}")
        # try:
        multis = update_weight(best_black, generations, number_of_childrens)
        best_black = fitness(multis, number_of_ancestors)
        # except Exception as e:
        #     print(e)
        i += 1

    print(best_black)
    print("END")
    # get_best_move(multiplicators)