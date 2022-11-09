import socket

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.back.domain.entities.player import Participant as ParticipantEntity
from src.back.domain.entities.player import ParticipantRegistration
from src.back.domain.entities.player import Player as PlayerEntity
from src.back.domain.entities.player import PlayerRegistration
from src.back.domain.exceptions import UnavailableRepositoryError
from src.back.domain.repositories.player import ParticipantRepository, PlayerRepository
from src.back.implementation.sqlite.models.player import Participant as ORMParticipant
from src.back.implementation.sqlite.models.player import Player as ORMPlayer


def orm_player_entity_adapter(database_player_model: ORMPlayer) -> PlayerEntity:
    if not database_player_model:
        return None
    return PlayerEntity(
        id=database_player_model.id,
        name=database_player_model.name,
        color=database_player_model.color,
    )


def player_entity_orm_adapter(player_entity: PlayerEntity) -> ORMPlayer:
    if not player_entity:
        return None
    return ORMPlayer(
        name=player_entity.name,
        color=player_entity.color,
    )


def orm_participant_entity_adapter(database_participant_model: ORMParticipant) -> ParticipantEntity:
    if not database_participant_model:
        return None
    return PlayerEntity(
        id=database_participant_model.id,
        game_id=database_participant_model.game_id,
        player_id=database_participant_model.player_id,
    )


class SQLitePlayerRepository(PlayerRepository):
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def _fetch_data(self, lookup):
        try:
            return await self.database_session.execute(lookup)
        except socket.gaierror:
            raise UnavailableRepositoryError()

    async def create_player(self, player: PlayerRegistration) -> PlayerEntity:
        player = ORMPlayer(
            name=player.name,
            color=player.color,
        )
        self.database_session.add(player)

        try:
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(player)
        # convert ORM data to domain entity
        return orm_player_entity_adapter(player)

    async def find_player_by_id(self, player_id: int) -> PlayerEntity:
        lookup = select(ORMPlayer).filter(ORMPlayer.id == player_id)
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        return orm_player_entity_adapter(db_user)


class SQLiteParticipantRepository(ParticipantRepository):
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def _fetch_data(self, lookup):
        try:
            return await self.database_session.execute(lookup)
        except socket.gaierror:
            raise UnavailableRepositoryError()

    async def create_participant(self, participant: ParticipantRegistration) -> ParticipantEntity:
        participant = ORMParticipant(
            score=participant.score,
        )
        print(participant.__dict__)
        self.database_session.add(participant)

        try:
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(participant)
        # convert ORM data to domain entity
        return orm_participant_entity_adapter(participant)

    async def find_participant_by_id(self, participant_id: int) -> ParticipantEntity:
        lookup = select(ORMParticipant).filter(ORMParticipant.id == participant_id)
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        return orm_participant_entity_adapter(db_user)
