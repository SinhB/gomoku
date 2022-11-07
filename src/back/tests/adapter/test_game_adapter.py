from datetime import datetime

import pytest
from freezegun import freeze_time
from src.back.domain.entities.game import Game as GameEntity
from src.back.domain.entities.game import GameCreationRequest
from src.back.implementation.game import SQLiteGameRepository


class TestSQLiteGameRepository:
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_init(self, testing_data_set_session):
        sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

        assert sqlite_game_repo.database_session == testing_data_set_session

    # @freeze_time("2042-05-24")
    # @pytest.mark.asyncio
    # async def test_sqlite_game_repo_start_no_player(self, testing_data_set_session):
    #     sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

    #     created_game = await sqlite_game_repo.start_game(
    #         GameCreationRequest(
    #             players=[],
    #             start_time=datetime.now(),
    #             max_number_of_players=2,
    #             number_of_turns=0,
    #             board_dimensions="19x19",
    #         )
    #     )

    #     assert created_game == GameEntity(
    #         id=created_game.id,
    #         players=[],
    #         start_time=datetime.now(),
    #         max_number_of_players=2,
    #         number_of_turns=0,
    #         board_dimensions="19x19",
    #     )

    @freeze_time("2042-05-24")
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_start_with_players(self, testing_data_set_session, player_one, player_two):
        sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

        created_game = await sqlite_game_repo.start_game(
            GameCreationRequest(
                players=[player_one, player_two],
                start_time=datetime.now(),
                max_number_of_players=2,
                number_of_turns=0,
                board_dimensions="19x19",
            )
        )

        assert created_game == GameEntity(
            id=created_game.id,
            players=[],
            start_time=datetime.now(),
            max_number_of_players=2,
            number_of_turns=0,
            board_dimensions="19x19",
        )
