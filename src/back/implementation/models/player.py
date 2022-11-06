from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from src.back.core.database import Base

participants = Table(
    "participants",
    Base.metadata,
    Column("game_id", ForeignKey("game.id"), primary_key=True),
    Column("player_id", ForeignKey("player.id"), primary_key=True),
)


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True)
    stone_color: Column(String)
    games = relationship("Game", secondary=participants, back_populates="players")
