"""
Defines all use cases for our system.

"""

from src.back.domain.repositories.game import GameRepository
from src.back.domain.schemas.game import Game, Stone
from src.back.domain.schemas.player import Player


class StartGameUseCase:
    def __init__(self, game: GameRepository) -> None:
        self._game = game

    def __call__(self, player_one: Player, player_two: Player) -> None:
        ...


class PlacingStoneUseCase:
    def __call__(self, game: Game, stone: Stone) -> None:
        ...
