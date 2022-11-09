from datetime import datetime

import pytest
from freezegun import freeze_time
from sqlalchemy import select
from src.back.domain.entities.game import Game as GameEntity
from src.back.domain.entities.game import GameCreationRequest
from src.back.domain.exceptions import MissingParameterError
from src.back.implementation.sqlite.game import SQLiteGameRepository
from src.back.implementation.sqlite.models.player import Participant as ORMParticipant


class TestSQLiteGameRepository:
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_init(self, testing_data_set_session):
        sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

        assert sqlite_game_repo.database_session == testing_data_set_session

    @freeze_time("2042-05-24")
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_start_no_player(self, testing_data_set_session):
        """
        Test that we can't start (store a game in db) when wrong/missing parameters are passed.
        """
        sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

        with pytest.raises(MissingParameterError):
            await sqlite_game_repo.start_game(
                GameCreationRequest(
                    players=[],
                    start_time=datetime.now(),
                    max_number_of_players=2,
                    number_of_turns=0,
                    board_dimensions="19x19",
                )
            )

    @freeze_time("2042-05-24")
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_start_with_players(self, testing_data_set_session, player_one, player_two):
        """
        Test that we can start (store a game in db) when valid parameters are passed.
        """
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

        stmt = select(ORMParticipant).where(ORMParticipant.player_id.in_([player_one.id, player_two.id]))
        result = await testing_data_set_session.execute(stmt)
        participants = result.scalars()

        assert created_game == GameEntity(
            id=created_game.id,
            players=[participant for participant in participants],
            start_time=datetime.now(),
            max_number_of_players=2,
            number_of_turns=0,
            board_dimensions="19x19",
        )

    @freeze_time("2042-05-24")
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_find_game_by_existing_id(self, testing_data_set_session, player_one, player_two):
        """
        Test that we can find an existing game by id in db.
        """
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

        stmt = select(ORMParticipant).where(ORMParticipant.player_id.in_([player_one.id, player_two.id]))
        result = await testing_data_set_session.execute(stmt)
        participants = result.scalars()

        retrieved_game = await sqlite_game_repo.find_game_by_id(created_game.id)

        assert retrieved_game == GameEntity(
            id=retrieved_game.id,
            players=[participant for participant in participants],
            start_time=datetime.now(),
            max_number_of_players=2,
            number_of_turns=0,
            board_dimensions="19x19",
        )

    @freeze_time("2042-05-24")
    @pytest.mark.asyncio
    async def test_sqlite_game_repo_do_not_find_game_with_non_existing_id(
        self, testing_data_set_session, player_one, player_two
    ):
        """
        Test that we can find an existing game by id in db.
        """
        sqlite_game_repo = SQLiteGameRepository(database_session=testing_data_set_session)

        retrieved_game = await sqlite_game_repo.find_game_by_id(42)
        assert retrieved_game is None
