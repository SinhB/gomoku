"""
Defines all use cases for our system.

"""
from dataclasses import dataclass

from src.back.domain.entities.game import GameCreationRequest
from src.back.domain.repositories.game import GameRepository
from src.back.domain.schemas.game import GameBase, Stone


@dataclass
class StartGameUseCase:
    repository: GameRepository

    async def __call__(self, game_creation_request: GameCreationRequest) -> GameBase:
        return await self.repository.start_game(game_creation_request)


@dataclass
class PlacingStoneUseCase:
    def __call__(self, game: GameBase, stone: Stone) -> None:
        ...
