import pandas as pd
import numpy as np
import pygame
from pygame.locals import *
from Helper import *


class _CandleBody():
    """ Draws the candle body wicks separately """

    def __init__(self, o: float, c: float) -> None:
        self.o = o
        self.c = c

    def draw(self, parent_surface: pygame.Surface, x_pos: int) -> None:
        positive = True if self.c > self.o else False
        color = GREEN if positive > 0 else RED
        start_y = ss(self.c if positive > 0 else self.o)
        length = max(1, screen_scale(abs(self.c - self.o)))
        rect = pygame.Rect((x_pos, start_y), (CANDLE_WIDTH,  length))
        pygame.draw.rect(surface=parent_surface, color=color, rect=rect)


class _CandleWicks():
    """ Draws the high and low wicks separately """

    def __init__(self, h: float, l: float, o: float, c: float) -> None:
        self.o = o
        self.c = c
        self.h = h
        self.l = l

    @property
    def positive(self) -> bool:
        # Keep track of the candle if positive or negative
        return True if self.c - self.o > 0 else False

    def draw(self, parent_surface: pygame.Surface, x_pos: int) -> None:
        color = GREEN if self.positive else RED
        x_pos = x_pos + int(CANDLE_WIDTH / 2)
        upper_wick_y_start = ss(self.h)
        upper_wick_y_end = ss(self.c if self.positive else self.o)

        lower_wick_y_start = ss(self.l)
        lower_wick_y_end = ss(self.o if self.positive else self.c)

        pygame.draw.line(surface=parent_surface, color=color, start_pos=(x_pos, upper_wick_y_start), end_pos=(x_pos, upper_wick_y_end))
        pygame.draw.line(surface=parent_surface, color=color, start_pos=(x_pos, lower_wick_y_start), end_pos=(x_pos, lower_wick_y_end))


class Candle():
    """ This class will return a candle object that can then be placed.
        NOTE: this should get a normalized series"""

    def __init__(self, series: pd.Series) -> None:
        self.o = series['Open']
        self.c = series['Close']
        self.h = series['High']
        self.l = series['Low']
        self.datetime = series['CloseTime']

    def draw(self, parent_surface: pygame.Surface, x_pos: int) -> None:
        # print(f'Candle: {self.np_array}')
        _CandleBody(o=self.o, c=self.c).draw(parent_surface, x_pos)
        _CandleWicks(o=self.o, c=self.c, h=self.h, l=self.l).draw(parent_surface, x_pos)

    @property
    def np_array(self):
        # Returns for now OHLC
        return np.array([self.o, self.h, self.l, self.c], dtype=float)
