from enum import Enum


class StoneColorEnum(str, Enum):
    BLACK = "black"
    WHITE = "white"


class PlayerTypeEnum(str, Enum):
    AI = "ai"
    HUMAN = "human"
