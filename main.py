"""Run a Gomoku Ninuki game"""

import sys
from src.algorithm import get_best_move
from src.board import BoardState
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

if __name__ =="__main__":
    board = BoardState(Color.BLACK, size=19)
    board.add_stone_coordinates([3, 6])
    print(board.coordinates)
    print(board.color)
    board = board.next(get_best_move(board, 2))
    print(board.color)
    board = board.next([3, 4])
    print(board.color)
    board = board.next([4, 5])
    print(board.color)
    board = board.next([5, 8])
    print(board.color)
    board = board.next([6, 9])
    print(board.color)
    board = board.next([2, 7])
    print(board.color)
    board = board.next([3, 7])
    print(board.color)
    board = board.next([3, 5])
    print(board.color)
    board = board.next([0, 8])
    print(board.color)
    board = board.next([10,10])
    print(board.color)
    board = board.next(get_best_move(board, 2))
    print(board.color)
    board.display()
    board = board.next(get_best_move(board, 2))
    sys.exit()