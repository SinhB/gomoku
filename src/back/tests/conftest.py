from pytest import fixture
from src.back.domain.entities.player import Player


@fixture
def player_one():
    return Player(id=0, name="Sinh", color="white")


@fixture
def player_two():
    return Player(id=1, name="Synkied", color="black")
