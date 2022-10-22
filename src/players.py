"""Class Players"""

from typing import List

from src.utils import Color
from stone import Stone


class Player:
    """
    A gomoku awesome/handsome player

    Attributes:
        - color(Color): Not the player skin color but the stone's color
            he/she chooses at the start of the game
        - prisoners(List[Stone]): List of stones the player captured
        - stones(List[Stone]): List of stones the player owns
    """

    def __init__(self, color) -> None:
        self.color: Color = color
        self.prisoners: List[Stone] = []
        self.stones: List[Stone] = []

    def add_prisoner(self, prisoner: Stone):
        """Add a stone in prisoners list"""
        self.prisoners.append(prisoner)

    def add_stone(self, stone: Stone):
        """Add a stone to the list"""
        self.stones.append(stone)
