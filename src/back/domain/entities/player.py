from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    color: str


@dataclass
class PlayerRegistration:
    name: str
    color: str
