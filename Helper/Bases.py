from __future__ import annotations
import pygame
import enum
import pandas as pd
from abc import ABC, abstractclassmethod
from typing import List

class Coordinate:
    """ Simple class to determine a cooridnate """
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class DrawBase(ABC):
    """ Abstract class that enforces a draw method """
    @abstractclassmethod
    def draw(self, parent_surface: pygame.Surface) -> pygame.Surface:
        raise NotImplementedError

class Position(enum.Enum):
	""" Class to make code more readable """
	EMPTY = 0
	LONG = 1

class Action(enum.Enum):
	""" Class to make code more readable """
	SELL = 0
	HOLD = 1
	BUY = 2

	@classmethod
	def get_action(cls, action: int) -> Action:
		""" Returns Action from the provided int value """
		assert(action in [0, 1, 2]), "Action must be in 0-2"
		if action == 0:
			return Action.SELL
		elif action == 1:
			return Action.HOLD
		elif action == 2:
			return Action.BUY
	
	@staticmethod
	def get_actions_list() -> List[str]:
		return ['SELL', 'HOLD', 'BUY']