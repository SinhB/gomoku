"""Run a Gomoku Ninuki game"""

import sys
from src.board import BoardState
from src.utils import Color

"""Only for windows"""
import colorama
colorama.init()

if __name__ =="__main__":
    board = BoardState(Color.BLACK, size=19)
    board.add_stone_coordinates(Color.BLACK, [3, 6])
    board.add_stone_coordinates(Color.WHITE, [3, 4])
    board.add_stone_coordinates(Color.WHITE, [4, 5])
    board.add_stone_coordinates(Color.BLACK, [5, 8])
    board.add_stone_coordinates(Color.BLACK, [6, 9])
    board.add_stone_coordinates(Color.BLACK, [2, 7])
    board.add_stone_coordinates(Color.BLACK, [1, 8])
    board.add_stone_coordinates(Color.BLACK, [3, 7])
    board.add_stone_coordinates(Color.BLACK, [3, 5])
    board.add_stone_coordinates(Color.BLACK, [0, 8])
    board.update()
    board.display()
    board.get_sequence_frequences()
    board.place_available_pos()
    board.display()
    print(f"NEXT STEP")
    bis = board.next([10,10])
    if bis:
        bis.display()
    else:
        print("NONE")
    sys.exit()