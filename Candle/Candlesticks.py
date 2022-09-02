import pandas as pd
from .Candlestick import Candle
import pygame
import time
from Helper import *

class CandleSticks(DrawBase):
    """ Use to draw candlesticks """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df
   
    def draw(self, parent_surface: pygame.Surface) -> pygame.Surface:
        x_pos = 0
        for _, row in self.df.iloc[-MAX_CANDLES_ON_DISPLAY:].iterrows():
            Candle(series=row).draw(parent_surface=parent_surface, x_pos=x_pos)
            x_pos += (CANDLE_WIDTH + INTER_CANDLE_GAP)
        return parent_surface
