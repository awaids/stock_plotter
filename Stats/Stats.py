import pandas as pd
import pygame
from Helper import Bases, Functions
from Helper.Contants import *

class Stats(Bases.DrawBase):
    def __init__(self, df:pd.DataFrame) -> None:
        self.df = df
    
    def get_font_screen(self, text:str, color: tuple=WHITE) -> pygame.Surface:
        my_font = pygame.font.SysFont(name='Comic Sans MS', size=12)
        return my_font.render(text, False, color)

    def draw(self, parent_surface: pygame.Surface) -> pygame.Surface:
        last_open = self.df['Open'].iat[-1]
        last_close = self.df['Close'].iat[-1]
        color = RED if last_open > last_close else GREEN
        y_pos = Functions.ss(last_close)
        x_start, x_end = 0, DISPLAY_X-1
        pygame.draw.line(surface=parent_surface, color=color, start_pos=(x_start, y_pos), end_pos=(x_end, y_pos))
        # Add text for close
        text_surface = self.get_font_screen(str(round(last_close, 4)), color)
        parent_surface.blit(text_surface, (0,y_pos))
        return parent_surface

