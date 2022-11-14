"""
Defines our interfaces/ports for game.
"""

from abc import ABC, abstractmethod

from src.back.domain.entities.game import Game, GameCreationRequest


class GameRepository(ABC):
    @abstractmethod
    async def start_game(self, game_start_request: GameCreationRequest) -> Game:
        ...

    @abstractmethod
    async def find_game_by_id(self, game_id: int) -> Game:
        ...
