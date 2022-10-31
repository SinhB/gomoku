"""Class Game

Response body:

{
    "turn": int,
    "legal": Bool,
    "game_status": {
        "positions": {
            "black": List[[int, int]],
            "white": List[[int, int]]
        },
        "finished": {
            "victory": bool,
            "type": ["capture", "alignement"],
            "winner": int #(color)
        },
        "players": {
            "black": {
                "score": int,
                "stones": int #(captured)
            },
            "white":{
                "score": int,
                "stones": int #(captured)
            }
        }
    }
}
"""

from players import IA, Player
from src.board import BoardState


class Game:
    """ """

    def __init__(self, player_one: Player, player_two: Player, depth=4) -> None:
        self.player_one: player_one
        self.player_two: player_two
        self.state = BoardState(19)
        self.depth = depth

    def start(self):
        pass

    def human_turn(self, position):
        if not self.state.is_legal_move(position):
            return False
        self.state = self.state.next(position)
        self.finished = self.state.is_finished()
        return True

    def ai_turn(self):
        position = self.state.get_best_move()
        self.state = self.state.next(position)
        self.finished = self.state.is_finished()
        return True
