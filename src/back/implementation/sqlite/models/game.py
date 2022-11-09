from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from src.back.core.database import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, index=True, primary_key=True)
    max_number_of_players = Column(Integer, default=2)
    number_of_turns = Column(Integer, default=0)
    board_dimensions = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    players = relationship("Participant", back_populates="game")
