"""
Defines our interfaces/ports for game.
"""

from abc import ABC, abstractmethod

from src.back.domain.entities.game import Game


class GameRepository(ABC):
    @abstractmethod
    def start_game(self) -> Game:
        ...

    @abstractmethod
    def find_game_by_id(self, game_id: int) -> Game:
        ...
