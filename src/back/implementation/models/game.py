from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from src.back.core.database import Base
from src.back.implementation.models.player import participants


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, index=True, primary_key=True)
    max_number_of_players = Column(Integer)
    number_of_turns = Column(Integer)
    board_dimensions = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    players = relationship("Player", secondary=participants, back_populates="games")
