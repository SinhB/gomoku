"""Class Game"""

from board import Board
from players import IA, Player


class Game:
    """ """

    def __init__(self, player_one: Player, player_two: Player) -> None:
        self.player_one: player_one
        self.player_two: player_two
        self.board = Board(19)

    def start(self):
        pass
