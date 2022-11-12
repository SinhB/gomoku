from datetime import datetime

from freezegun import freeze_time

from src.back.domain.entities.game import Game


@freeze_time("2042-05-24")
def test_game_init():
    game = Game(id=42, start_time=datetime.now())
    assert game.number_of_turns == 0
