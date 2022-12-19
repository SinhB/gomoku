from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import numpy as np
import time
import json

import board_utils
import board_functions
import get_move
import get_threats

from check_breakable import check_if_breakable

## FOR WINDOWS TERM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def check_line_win(arr, seq):
    # Check for sequence in the flatten board
    seq_len = len(seq)
    upper_bound = len(arr) - seq_len + 1
    for i in range(upper_bound):
        
        if board_utils.is_array_equal(arr[i : i + seq_len], seq):
            return True

    return False

def check_win(board, position, player, total_eat, total_enemy_eat):
    if total_eat >= 5:
        print("Win by eating")
        return True, None
    row_index = position[0]
    col_index = position[1]

    win_array = np.array((player, player, player, player, player))

    lr_diags, rl_diags, rows, columns = board_utils.get_vectors(board, row_index, col_index)


    if check_line_win(lr_diags, win_array):
        lr_starting_index = col_index if row_index > col_index else row_index
        is_breakable, breaking_pos = check_if_breakable(board, 0, lr_diags, lr_starting_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            print("Win by alignment")
            return True, None
    if check_line_win(rl_diags, win_array):
        rl_starting_index = 18 - col_index if row_index > 18 - col_index else row_index
        is_breakable, breaking_pos = check_if_breakable(board, 1, rl_diags, rl_starting_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            print("Win by alignment")
            return True, None
    if check_line_win(rows, win_array):
        is_breakable, breaking_pos = check_if_breakable(board, 2, rows, col_index, player, row_index, col_index)
        print(is_breakable)
        print(breaking_pos)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            print("Win by alignment")
            return True, None
    if check_line_win(columns, win_array):
        is_breakable, breaking_pos = check_if_breakable(board, 3, columns, row_index, player, row_index, col_index)
        if is_breakable and total_enemy_eat == 4:
            return False, breaking_pos
        else:
            print("Win by alignment")
            return True, None
    return False, None

class Env:

    def __init__(self):
        self.board = board_functions.init_board(19)
        self.total_eat = {-1: 0, 1: 0}
        self.empty_board = True
        self.priority_move = {-1: None, 1: None}

    def reset(self):
        self.board = board_functions.init_board(19)
        self.total_eat = {-1: 0, 1: 0}
        self.empty_board = True
        self.priority_move = {-1: None, 1: None}

rooms = {}

@app.get("/init")
def init(room: str):
    rooms[room] = Env()

@app.get("/get_best_move")
def get_best_move(player: int, depth: int, room: str, cutoff: int, quick_play: bool):
    one_move_timer = time.time()
    if rooms[room].priority_move[player] is not None:
        next_move = rooms[room].priority_move[player]
    else:
        initial_board = np.copy(rooms[room].board)
        next_move = get_move.get_next_move(initial_board, depth, True, player, rooms[room].total_eat, rooms[room].empty_board, cutoff / 10, quick_play)
    one_move_timer_stop = time.time()
    if type(next_move) != list:
        next_move = next_move.tolist()
    return {"best_move": next_move, "timer": one_move_timer_stop - one_move_timer}

@app.get("/apply_move")
def apply_move(player: int, move: str, room: str):
    move = [int(x) for x in move.split(',')]

    rooms[room].empty_board = False

    if rooms[room].priority_move[player] is not None and rooms[room].priority_move[player].tolist() == move:
        print(move, type(move))
        print(rooms[room].priority_move[player].tolist(), type(rooms[room].priority_move[player].tolist()))
        rooms[room].priority_move[player] = None
    try:
        rooms[room].board, eat, eaten_pos = board_functions.place_stone(rooms[room].board, move, player)
    except board_functions.ForbiddenMove:
        ret_total_eat = {'black': rooms[room].total_eat[1], 'white': rooms[room].total_eat[-1]}
        return {'forbidden_move': True, "win": False, "total_eat": ret_total_eat, 'eaten_pos': json.dumps({"eaten_pos": []})}
    rooms[room].total_eat[player] += eat

    ret_total_eat = {'black': rooms[room].total_eat[1], 'white': rooms[room].total_eat[-1]}

    board_functions.print_board(rooms[room].board, move)

    is_win, breaking_pos = check_win(rooms[room].board, move, player, rooms[room].total_eat[player], rooms[room].total_eat[-player])
    if breaking_pos is not None:
        rooms[room].priority_move[-player] = breaking_pos
    if is_win:
        board_functions.print_board(rooms[room].board, move)
        print(f"Player {player} ({'B' if player == -1 else 'N'}) won the game")
        return {'forbidden_move': False, "win": True, "total_eat": ret_total_eat, "eaten_pos": json.dumps({"eaten_pos": eaten_pos})}
    else:
        return {'forbidden_move': False, "win": False, "total_eat": ret_total_eat, "eaten_pos": json.dumps({"eaten_pos": eaten_pos})}

if __name__ == "__main__":
    with open('../network.json', 'r') as f:
        data = json.load(f)
    address = data['address']
    uvicorn.run("gomoku_server:app", host=address, port=5000, log_level="info", reload=True)
    # uvicorn.run("gomoku_server:app", port=5000, log_level="info", reload=True)