from datetime import datetime

from src.back.implementation.models.game import Game as ORMGame
from src.back.implementation.models.player import Player as ORMPlayer

TESTING_ORM_USER_1 = ORMPlayer(
    id=42,
    name="Sinh",
    color="white",
)

TESTING_ORM_USER_2 = ORMPlayer(
    id=3,
    name="Synkied",
    color="black",
)

TESTING_ORM_GAME = ORMGame(
    max_number_of_players=2,
    number_of_turns=0,
    board_dimensions="19x19",
    start_time=datetime.now(),
    players=2,
)
