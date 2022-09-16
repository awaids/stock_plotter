import pandas as pd
from .Candlestick import Candle
from stock_plotter.Helper import *
from stock_plotter.Surface import StockSurface

class CandleSticks():
    """ Use to draw candlesticks """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df
        self.last_x_pos = 0
   
    def draw(self, stockSurface:StockSurface) -> None:
        x_pos = 0
        for _, row in self.df.iloc[-MAX_CANDLES_ON_DISPLAY:].iterrows():
            Candle(series=row).draw(parent_surface=stockSurface.surface, x_pos=x_pos)
            x_pos += (CANDLE_WIDTH + INTER_CANDLE_GAP)
            # This is required to keep track where the Traders will be drawn
            stockSurface.last_x_pos = x_pos