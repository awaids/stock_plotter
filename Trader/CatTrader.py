import pygame
from os.path import dirname, join
from Helper import DrawBase

class CatTrader(DrawBase):
    def __init__(self) -> None:
        image = pygame.image.load(join(dirname(__file__), "TraderCat.png")).convert()
        self.image = pygame.transform.scale(image, (50, 50))

    def draw(self, parent_surface: pygame.Surface) -> pygame.Surface:
        parent_surface.blit(self.image, (0,0))
        return parent_surface