import pygame
from typing import Tuple, List
from ..Helper.Contants import *

class StockSurface:
    pygame.init()
    pygame.font.init()
    Border_width = 2

    def reset(self) -> None:
        pygame.display.set_caption(self._caption)
        self._surface = pygame.display.set_mode((self._x_size, self._y_size))
        self._font = pygame.font.SysFont(None, self._font_size)
        self._surface.fill(BOARD_BACKGROUND_COLOR)

        # Maintain the last x_postion
        self._last_x_pos = 0

    def __init__(self, caption:str="Default", x_size:int=DISPLAY_X, y_size:int=DISPLAY_Y) -> None:
        # Setup the display
        self._caption = caption
        self._x_size = x_size
        self._y_size = y_size
        # hardcoding the font size here
        self._font_size = 25

        # Configure the useable screen
        # TODO: use these here
        self.usebale_width = x_size - 2 * self.Border_width
        self.usebale_heigth = y_size - 2 * self.Border_width

        self.reset()

    @property
    def screen_width(self) -> int:
        return self.surface.get_size()[0]
    
    @property
    def screen_height(self) -> int:
        return self.surface.get_size()[1]

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @property
    def last_x_pos(self) -> int:
        return self._last_x_pos

    @last_x_pos.setter
    def last_x_pos(self, value:int) -> int:
        assert(value >= 0), "X value cannot be negative"
        self._last_x_pos = value

    def show_display(self) -> None:
        pygame.display.flip()
    
    def clear_display(self) -> None:
        self._surface.fill(BOARD_BACKGROUND_COLOR)

    def draw_line(self, color, start: Tuple[int,int], end: Tuple[int,int]) -> None:
        pygame.draw.line(self.surface, color, start, end, width=1)

    def draw_vertical_line(self, x_pos:int, color=WHITE) -> None:
        self.draw_line(color=color, start=(x_pos,0), end=(x_pos, self.screen_height))

    def add_image(self, image:pygame.Surface, pos: Tuple[int,int], opacity:bool=False) -> None:
        if opacity:
            image.set_alpha(100)
        self.surface.blit(image, pos)
    
    def add_text(self, text:str, color, pos, opacity:bool) -> None:
        image = self._font.render(text, True, color)
        if opacity:
            image.set_alpha(100)
        self._surface.blit(image, pos)

    def add_multline_text(self, lines:List[Tuple[str, Tuple]], pos, opacity:bool = False) -> None:
        x_pos, y_pos = pos
        for line, color in lines:
            self.add_text(line, color, (x_pos, y_pos), opacity)
            y_pos += (self._font_size / 1.5 )


    @staticmethod
    def load_image(path:str, size: Tuple[int,int]) -> pygame.Surface:
        assert(pygame.get_init()), "pygame not initialized"

        for s in size:
            assert(s > 0), "Image provided size must be greater than 0"
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
