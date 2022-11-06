import pytest
from src.back.core.database import use_database
from src.back.implementation.game import SQLiteGameRepository


class TestSQLiteGameRepository:
    @pytest.mark.asyncio
    async def test_game_start(self):
        async with use_database() as session:
            sqlite_game_repo = SQLiteGameRepository(database_session=session)

        assert sqlite_game_repo.database_session == session
