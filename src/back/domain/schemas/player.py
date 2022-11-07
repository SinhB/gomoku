from pydantic import BaseModel, PositiveInt
from src.back.core.constants import StoneColorEnum


class Player(BaseModel):
    id: PositiveInt
    name = "John Doe"
    color: StoneColorEnum
