import pygame
from .Contants import *

def setup_disply(caption: str = 'Stock Plotter') -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption(caption)
    surface = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    surface.fill(BOARD_BACKGROUND_COLOR)
    # This is required for printing text
    
    return surface

def clear_display(surface:pygame.Surface) -> pygame.Surface:
    surface.fill(BOARD_BACKGROUND_COLOR)
    return surface

def show_display() -> None:
    pygame.display.flip()


def screen_scale(y:float) -> int:
    """ Returns a scaled value based on useable screen y-size """
    assert(y >= 0.0 and y <= 1.0), 'val should be between [0-1]'
    return round(y * USEABLE_Y_SCREEN)

#TODO: rename this to something more useful
def ss(y:float) -> int:
    """ Return a scaled and off-setted screen based on DISPLAY_Y_GAP,
        Translate the point to exact location. """
    assert(y >= 0.0 and y <= 1.0), 'val should be between [0-1]'
    return USEABLE_Y_SCREEN - screen_scale(y)

