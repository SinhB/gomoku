import socket

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.back.domain.entities.game import Game as GameEntity
from src.back.domain.entities.game import GameCreationRequest
from src.back.domain.entities.player import PlayerRegistration
from src.back.domain.exceptions import IdentityAlreadyInUse, UnavailableRepositoryError
from src.back.domain.repositories.game import GameRepository
from src.back.implementation.models.game import Game as ORMGame
from src.back.implementation.player import SQLitePlayerRepository


def orm_game_adapter(database_game_model: ORMGame) -> GameEntity:
    if not database_game_model:
        return None

    return GameEntity(
        id=database_game_model.id,
        players=database_game_model.players,
        start_time=database_game_model.start_time,
        max_number_of_players=database_game_model.max_number_of_players,
        number_of_turns=database_game_model.number_of_turns,
        board_dimensions=database_game_model.board_dimensions,
    )


class SQLiteGameRepository(GameRepository):
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def start_game(self, game_start_request: GameCreationRequest) -> GameEntity:
        sqlite_player_repo = SQLitePlayerRepository(database_session=self.database_session)
        player_one = await sqlite_player_repo.create_player(
            PlayerRegistration(name=game_start_request.players[0].name, color=game_start_request.players[0].color)
        )
        player_two = await sqlite_player_repo.create_player(
            PlayerRegistration(name=game_start_request.players[1].name, color=game_start_request.players[0].color)
        )

        db_game = ORMGame(
            board_dimensions=game_start_request.board_dimensions,
            start_time=game_start_request.start_time,
            players=[player_one, player_two],
        )
        self.database_session.add(db_game)

        try:
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()
        except IntegrityError:
            raise IdentityAlreadyInUse()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(db_game)
        # convert ORM data to domain entity
        print(db_game.__dict__)
        return orm_game_adapter(db_game)

    def find_game_by_id(self, game_id: int) -> GameEntity:
        ...
