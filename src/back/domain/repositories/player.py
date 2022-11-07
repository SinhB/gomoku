"""
Defines our interfaces/ports for player.
"""

from abc import ABC, abstractmethod

from src.back.domain.entities.player import Player


class PlayerRepository(ABC):
    @abstractmethod
    def create_player(self) -> Player:
        ...

    @abstractmethod
    def find_player_by_id(self, game_id: int) -> Player:
        ...
