"""Run a Gomoku Ninuki game"""

import sys
from src.board import Board
from src.stone import Stone
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

if __name__ =="__main__":
    board = Board(19)
    s1 = Stone(Color.BLACK, [3, 6])
    s2 = Stone(Color.WHITE, [3, 4])
    s3 = Stone(Color.WHITE, [3, 5])
    board.add_stone_coordinates(s1)
    board.add_stone_coordinates(s2)
    board.add_stone_coordinates(s3)
    board.update()
    board.display()
    sys.exit()