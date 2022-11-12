from dataclasses import asdict, dataclass


@dataclass
class Player:
    id: int
    name: str
    color: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


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
