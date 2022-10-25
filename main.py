"""Run a Gomoku Ninuki game"""

import sys
from src.board import Board
from src.stone import Stone
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()


if __name__ =="__main__":
    board = Board(Color.BLACK, 19)
    s1 = Stone(Color.BLACK, [3, 6])
    s2 = Stone(Color.WHITE, [3, 4])
    s3 = Stone(Color.WHITE, [4, 5])
    s4 = Stone(Color.BLACK, [5, 8])
    s5 = Stone(Color.BLACK, [6, 9])
    s6 = Stone(Color.BLACK, [2, 7])
    s7 = Stone(Color.BLACK, [1, 8])
    s8 = Stone(Color.BLACK, [3, 7])
    s9 = Stone(Color.BLACK, [3, 5])
    board.add_stone_coordinates(s1)
    board.add_stone_coordinates(s2)
    board.add_stone_coordinates(s3)
    board.add_stone_coordinates(s4)
    board.add_stone_coordinates(s5)
    board.add_stone_coordinates(s6)
    board.add_stone_coordinates(s7)
    board.add_stone_coordinates(s8)
    board.add_stone_coordinates(s9)
    board.update()
    board.display()
    board.get_score()
    # b, w = board.get_stones_coordinates()
    # print(b)
    # print(w)
    board.place_available_pos()
    board.display()
    sys.exit()