from src.back.domain.entities.game import Game


def test_game_init(player_one, player_two):
    game = Game(
        player_one,
        player_two,
    )
    assert game.number_of_turns == 0
    assert game.player_one == player_one
    assert game.player_two == player_two
    assert game.player_one.stone_color == "white"
    assert game.player_two.stone_color == "black"
