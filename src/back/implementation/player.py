import socket

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.back.domain.entities.player import Player as PlayerEntity
from src.back.domain.entities.player import PlayerRegistration
from src.back.domain.exceptions import IdentityAlreadyInUse, UnavailableRepositoryError
from src.back.domain.repositories.player import PlayerRepository
from src.back.implementation.models.player import Player as ORMPlayer


def orm_player_adapter(database_player_model: ORMPlayer) -> PlayerEntity:
    if not database_player_model:
        return None
    return PlayerEntity(
        id=database_player_model.id,
        name=database_player_model.name,
        color=database_player_model.color,
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
        except IntegrityError:
            raise IdentityAlreadyInUse()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(player)
        # convert ORM data to domain entity
        return orm_player_adapter(player)

    async def find_player_by_id(self, player_id: int) -> PlayerEntity:
        lookup = select(ORMPlayer).filter(ORMPlayer.id == player_id)
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        return orm_player_adapter(db_user)
