"""
Defines all use cases for our system.

"""
from typing import Tuple

from src.back.domain.repositories.game import GameRepository
from src.back.domain.schemas.game import Game, Stone
from src.back.domain.schemas.player import Player


class StartGameUseCase:
    repository: GameRepository

    def __call__(self, players: Tuple[Player]) -> None:
        ...

    def start_game(self):
        self.repository.start_game()


class PlacingStoneUseCase:
    def __call__(self, game: Game, stone: Stone) -> None:
        ...


StartGameUseCase(repository=GameRepository()).start_game()
