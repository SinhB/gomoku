from src.back.core.database import use_database
from src.back.implementation.sqlite.game import SQLiteGameRepository


async def get_game_repository():
    async with use_database() as session:
        repository = SQLiteGameRepository(database_session=session)
        yield repository
