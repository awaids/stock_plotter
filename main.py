import pygame
from Helper import *
from Candle import CandleSticks
import time


def setup_disply() -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption('Stock Plotter')
    surface = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    surface.fill(BOARD_BACKGROUND_COLOR)
    return surface

def clear_display(surface:pygame.Surface) -> pygame.Surface:
    surface.fill(BOARD_BACKGROUND_COLOR)
    return surface

def main(simulate_live:bool=True) -> None:
    surface = setup_disply()
    df = read_csv('Stocks_Data/BTCUSDT_1d.csv', normalize=True)
    if simulate_live:
        for idx in range(df.shape[0]):
            clear_display(surface)
            live_df = df[:idx]
            CandleSticks(df=live_df).draw(parent_surface=surface)
            # Show display
            pygame.display.flip()
            time.sleep(0.05)
    else:
        CandleSticks(df=df).draw(parent_surface=surface)
        pygame.display.flip()

if __name__ == '__main__':
    main(simulate_live=True)
    time.sleep(5)