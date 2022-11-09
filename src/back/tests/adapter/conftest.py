import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.back.implementation.sqlite.models.game import Game as ORMGame
from src.back.implementation.sqlite.models.player import Player as ORMPlayer


@pytest_asyncio.fixture
async def testing_data_set_session():
    # We don't have complex queries. Using an "in memory" sqlite database
    # to avoid the need to spawn a psql database and keep performances high
    # while running tests.
    # NOTE: This is dangerous as sqlite and psql don't behave the same way.
    # This hack shall not be used on a production environment
    engine = create_async_engine("sqlite+aiosqlite://")

    async with engine.begin() as conn:
        await conn.run_sync(ORMGame.metadata.drop_all)
        await conn.run_sync(ORMGame.metadata.create_all)
        await conn.run_sync(ORMPlayer.metadata.drop_all)
        await conn.run_sync(ORMPlayer.metadata.create_all)

    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
