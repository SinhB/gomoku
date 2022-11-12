from datetime import datetime
from typing import Tuple

from pydantic import BaseModel, PositiveInt

from src.back.core.constants import StoneColorEnum
from src.back.domain.schemas.player import PlayerRegistration


class GameBase(BaseModel):
    id: PositiveInt
    max_number_of_players: PositiveInt = 2
    number_of_turns: PositiveInt = 0
    board_dimensions: str
    start_time: datetime
    end_time: datetime


class GameCreation(BaseModel):
    players: Tuple[PlayerRegistration, PlayerRegistration]
    start_time: datetime = datetime.now()
    max_number_of_players: int = 2
    number_of_turns: int = 0
    board_dimensions: str = "19x19"


class Stone(BaseModel):
    id: PositiveInt
    color: StoneColorEnum
    coordinates: Tuple[int, int]
