from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import numpy as np
import time
import json

import board_functions
import get_move
import get_lines
import get_threats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

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

def check_win(board, position, player, total_eat):
    if total_eat >= 5:
        print("Win by eating")
        return True
    row_index = position[0]
    col_index = position[1]

    win_array = (player, player, player, player, player)

    # lr_diags, rl_diags = get_lines.get_position_diagonals(board, row_index, col_index)
    # rows = get_lines.get_position_rows(board, row_index)
    # columns = get_lines.get_position_columns(board, col_index)
    lr_diags = np.diag(board, row_index - col_index)
    w = board.shape[1]
    rl_diags = np.diag(np.fliplr(board), w-col_index-1-row_index)
    rows = board[row_index, :]
    columns = board[:, col_index]

    if check_line_win(lr_diags, win_array):
        print("Win by alignment")
        return True
    if check_line_win(rl_diags, win_array):
        print("Win by alignment")
        return True
    if check_line_win(rows, win_array):
        print("Win by alignment")
        return True
    if check_line_win(columns, win_array):
        print("Win by alignment")
        return True
    return False

class Env:

    def __init__(self):
        self.board = board_functions.init_board(19)
        self.total_eat = {-1: 0, 1: 0}
        self.empty_board = True

    def reset(self):
        self.board = board_functions.init_board(19)
        self.total_eat = {-1: 0, 1: 0}
        self.empty_board = True

env = Env()

@app.get("/init")
def init():
    env.reset()
    return

@app.get("/get_best_move")
def get_best_move(player: int):
    one_move_timer = time.time()
    initial_board = np.copy(env.board)
    next_move = get_move.get_next_move(initial_board, 19, 10, True, player, env.total_eat, env.empty_board)
    one_move_timer_stop = time.time()
    if type(next_move) != list:
        next_move = next_move.tolist()
    return {"best_move": next_move, "timer": one_move_timer_stop - one_move_timer}

@app.get("/apply_move")
def apply_move(player: int, move: str):
    print(move)
    move = [int(x) for x in move.split(',')]
    print(move)
    env.empty_board = False

    env.board, eat, eaten_pos = board_functions.place_stone(env.board, move, player)
    env.total_eat[player] += eat

    ret_total_eat = {'BLACK': env.total_eat[1], 'WHITE': env.total_eat[-1]}

    board_functions.print_board(env.board, move)

    if check_win(env.board, move, player, env.total_eat[player]):
        board_functions.print_board(env.board, move)
        print(f"Player {player} ({'B' if player == -1 else 'N'}) won the game")
        return {"win": True, "total_eat": ret_total_eat, "eaten_pos": json.dumps({"eaten_pos": eaten_pos})}
        # return True, env.total_eat
    else:
        return {"win": False, "total_eat": ret_total_eat, "eaten_pos": json.dumps({"eaten_pos": eaten_pos})}

@app.get("/get_board")
def get_board():
    return {"board": env.board.tolist()}

if __name__ == "__main__":
    uvicorn.run("gomoku_server:app", port=5000, log_level="info", reload=True)
