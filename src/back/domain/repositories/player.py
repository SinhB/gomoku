"""
Defines our interfaces/ports for player.
"""

from abc import ABC, abstractmethod

from src.back.domain.entities.player import Participant, Player


class PlayerRepository(ABC):
    @abstractmethod
    def create_player(self) -> Player:
        ...

    @abstractmethod
    def find_player_by_id(self, player_id: int) -> Player:
        ...


class ParticipantRepository(ABC):
    @abstractmethod
    def create_participant(self) -> Participant:
        ...

    @abstractmethod
    def find_participant_by_id(self, participant_id: int) -> Participant:
        ...
