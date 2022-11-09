from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    color: str


@dataclass
class Participant:
    score: str
    game_id: int
    player_id: int


@dataclass
class PlayerRegistration:
    name: str
    color: str


@dataclass
class ParticipantRegistration:
    score: int = 0
