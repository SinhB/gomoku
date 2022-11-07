from src.back.domain.entities.game import Game


def test_game_init(player_one, player_two):
    game = Game(id=42, players=[player_one, player_two])
    assert game.number_of_turns == 0
    assert game.players == [player_one, player_two]
    assert game.players[0].color == "white"
    assert game.players[1].color == "black"
