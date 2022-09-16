import pygame
from Helper import *
from Candle import CandleSticks
from Stats import Stats
from Trader import CatTrader
import time

def main(simulate_live:bool=True) -> None:
    surface = setup_disply()
    stockData = StockDataDF(read_csv('Stocks_Data/BTCUSDT_1d.csv'))
    if simulate_live:
        for live_df in stockData.live_generator():
            clear_display(surface)
            CandleSticks(df=live_df).draw(parent_surface=surface)
            Stats(df=live_df).draw(parent_surface=surface)
            CatTrader().draw(parent_surface=surface)
            # Show display
            pygame.display.flip()
            time.sleep(0.05)
    else:
        CandleSticks(df=stockData.df).draw(parent_surface=surface)
        pygame.display.flip()

if __name__ == '__main__':
    main(simulate_live=True)
    time.sleep(5)