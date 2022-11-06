from sqlalchemy.ext.asyncio import AsyncSession
from src.back.domain.entities.game import Game
from src.back.domain.repositories.game import GameRepository
from src.back.implementation.models.game import Game as ORMGame


def orm_game_adapter(database_user_model: ORMGame) -> Game:
    if not database_user_model:
        return None
    return Game()


def game_orm_adapter(database_user_model: Game) -> ORMGame:
    ...


class SQLiteGameRepository(GameRepository):
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    def start_game(self) -> Game:
        ...

    def find_game_by_id(self, game_id: int) -> Game:
        ...
