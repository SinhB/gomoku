from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from src.back.domain.entities.player import Player


@dataclass(frozen=True, slots=True)
class Game:
    id: int
    start_time: datetime
    max_number_of_players: int = 2
    number_of_turns: int = 0
    board_dimensions: str = "19x19"


@dataclass(frozen=True, slots=True)
class GameCreationRequest:
    players: Tuple[Player, Player]
    start_time: datetime = datetime.now()
    max_number_of_players: int = 2
    number_of_turns: int = 0
    board_dimensions: str = "19x19"


@dataclass(frozen=True, slots=True)
class Stone:
    id: int
    color: str
    coordinates: Tuple[int, int]


@dataclass(frozen=True, slots=True)
class Board:
    id: int
    size: int
