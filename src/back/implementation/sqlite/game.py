import socket

from sqlalchemy.ext.asyncio import AsyncSession
from src.back.domain.entities.game import Game as GameEntity
from src.back.domain.entities.game import GameCreationRequest
from src.back.domain.entities.player import PlayerRegistration
from src.back.domain.exceptions import UnavailableRepositoryError
from src.back.domain.repositories.game import GameRepository
from src.back.implementation.sqlite.models.game import Game as ORMGame
from src.back.implementation.sqlite.models.player import Participant as ORMParticipant
from src.back.implementation.sqlite.player import player_entity_orm_adapter


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
        player_one = player_entity_orm_adapter(
            PlayerRegistration(name=game_start_request.players[0].name, color=game_start_request.players[0].color)
        )
        player_two = player_entity_orm_adapter(
            PlayerRegistration(name=game_start_request.players[1].name, color=game_start_request.players[1].color)
        )
        self.database_session.add(player_one)

        db_game = ORMGame(
            board_dimensions=game_start_request.board_dimensions,
            start_time=game_start_request.start_time,
        )
        self.database_session.add(db_game)

        participant_one = ORMParticipant(player=player_one, game=db_game)
        self.database_session.add(participant_one)

        participant_two = ORMParticipant(player=player_two, game=db_game)
        self.database_session.add(participant_two)

        # the refresh method allows us to get the ID back from DB's call
        try:
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

        # convert ORM data to domain entity
        return orm_game_adapter(db_game)

    def find_game_by_id(self, game_id: int) -> GameEntity:
        ...
