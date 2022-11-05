from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    stone_color: str
