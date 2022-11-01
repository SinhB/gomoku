"""Run a Gomoku Ninuki game"""

import sys
from src.board import BoardState
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

if __name__ =="__main__":
    board = BoardState(Color.BLACK, size=19)
    # board.add_stone_coordinates([3, 6])
    # print(board.coordinates)
    # print(board.color)
    # board.is_legal_move([3, 4])
    board = board.next([3, 4])
    # print(board.color)
    # board.is_legal_move([4, 5])
    board = board.next([4, 5])
    # print(board.color)
    # board.is_legal_move([5, 8])
    board = board.next([5, 8])
    # print(board.color)
    # board.is_legal_move([6, 9])
    board = board.next([6, 9])
    # print(board.color)
    # board.is_legal_move([2, 7])
    board = board.next([2, 7])
    # board.display()
    # print(board.color)
    # board.is_legal_move([3, 7])
    board = board.next([3, 7])
    # print(board.color)
    # board.is_legal_move([3, 5])
    board = board.next([3, 5])
    # print(board.color)
    # board.is_legal_move([0, 8])
    board = board.next([0, 8])
    # print(board.color)
    board.is_legal_move([10,10])
    board = board.next([10,10])
    board.display()
    print(f"COLOR BEFORE GET BEST MOVE: {board.color}")
    pos = board.get_best_move(10, True)
    print(pos)
    board = board.next(pos[0])
    board.display()
    print(f"NEW COLOR BEFORE GET BEST MOVE: {board.color}")
    pos = board.get_best_move(10, True)
    pos = board.get_best_move(5, True)
    print(pos)
    board = board.next(pos[0])
    board.display()

    sys.exit()