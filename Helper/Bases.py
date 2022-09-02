import pygame
from abc import ABC, abstractclassmethod

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