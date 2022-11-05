from pytest import fixture
from src.back.domain.entities.player import Player


@fixture
def player_one():
    return Player(id=0, name="Player One", stone_color="white")


@fixture
def player_two():
    return Player(id=1, name="Player Two", stone_color="black")
