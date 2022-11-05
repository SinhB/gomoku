from dataclasses import dataclass
from typing import Tuple

from src.back.domain.entities.player import Player


@dataclass(frozen=True, slots=True)
class Game:
    player_one: Player
    player_two: Player
    number_of_turns: int = 0


@dataclass(frozen=True, slots=True)
class Stone:
    id: int
    stone_color: str
    coordinates: Tuple[int, int]


@dataclass(frozen=True, slots=True)
class Board:
    id: int
    size: int
