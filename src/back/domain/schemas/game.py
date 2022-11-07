from datetime import datetime
from typing import Tuple

from pydantic import BaseModel, PositiveInt
from src.back.core.constants import StoneColorEnum


class Game(BaseModel):
    max_number_of_players: PositiveInt = 2
    number_of_turns: PositiveInt = 0
    board_dimensions: str
    start_time: datetime
    end_time: datetime


class Stone(BaseModel):
    id: PositiveInt
    color: StoneColorEnum
    coordinates: Tuple[int, int]
