from typing import Tuple

from pydantic import BaseModel, PositiveInt
from src.back.core.constants import StoneColorEnum
from src.back.domain.schemas.player import Player


class Game(BaseModel):
    player_one: Player
    player_two: Player
    number_of_turns: PositiveInt = 0


class Stone(BaseModel):
    id: PositiveInt
    stone_color: StoneColorEnum
    coordinates: Tuple[int, int]
