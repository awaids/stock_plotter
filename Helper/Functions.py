from .Contants import *

def screen_scale(y:float) -> int:
    """ Returns a scaled value based on useable screen y-size """
    assert(y >= 0.0 and y <= 1.0), 'val should be between [0-1]'
    return round(y * USEABLE_Y_SCREEN)

def ss(y:float) -> int:
    """ Return a scaled and off-setted screen based on DISPLAY_Y_GAP,
        Translate the point to exact location. """
    assert(y >= 0.0 and y <= 1.0), 'val should be between [0-1]'
    return USEABLE_Y_SCREEN - screen_scale(y)