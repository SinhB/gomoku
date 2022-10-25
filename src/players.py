"""Class Players"""

import numpy as np

from src.utils import Color


class Player:
    """
    A gomoku awesome/handsome player

    Attributes:
        - color(Color): Not the player skin color but the stone's color
            he/she chooses at the start of the game
        - prisoners(np.array): List of stones the player captured
        - stones(np.array): List of stones the player owns
    """

    def __init__(self, color) -> None:
        self.color: Color = color
        self.prisoners: np.array
        self.stones: np.array

    def add_prisoner(self, prisoner):
        """Add a stone in prisoners list"""
        self.prisoners.append(prisoner)

    def add_stone(self, stone):
        """Add a stone to the list"""
        self.stones.append(stone)


class IA(Player):
    """
    A gomoku IA inherit from Player class
    """

    def __init__(self, color) -> None:
        super().__init__(color)
