from datetime import datetime

from freezegun import freeze_time

from src.back.domain.entities.game import Game


@freeze_time("2042-05-24")
def test_game_init(player_one, player_two):
    game = Game(id=42, players=[player_one, player_two], start_time=datetime.now())
    assert game.number_of_turns == 0
    assert game.players == [player_one, player_two]
    assert game.players[0].color == "white"
    assert game.players[1].color == "black"
