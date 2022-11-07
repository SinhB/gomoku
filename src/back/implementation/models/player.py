from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.back.core.database import Base


class Participant(Base):
    __tablename__ = "participant"

    game_id = Column(ForeignKey("game.id"), primary_key=True)
    player_id = Column(ForeignKey("player.id"), primary_key=True)
    score = Column(Integer)
    player = relationship("Player", back_populates="games")
    game = relationship("Game", back_populates="players")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True)
    color = Column(String)
    games = relationship("Participant", back_populates="player")
