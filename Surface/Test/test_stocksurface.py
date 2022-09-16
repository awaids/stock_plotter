import pytest
from os.path import join, dirname
from time import sleep
from stock_plotter.Surface import StockSurface
from stock_plotter.Helper.Contants import *

class TestStockSurface:
    stockSurface = StockSurface(caption="Test", x_size=200, y_size=100)

    def test_screen_dim(self):
        assert(self.stockSurface.screen_height == 100), "Height not correct"
        assert(self.stockSurface.screen_width == 200), "Width not correct"

    def test_draw_line(self):
        self.stockSurface.draw_line(color=WHITE, start=(0,0),end=(200,100))
        self.stockSurface.show_display()

    def test_draw_vertical_line(self):
        self.stockSurface.draw_vertical_line(color=WHITE, x_pos=1)
        self.stockSurface.draw_vertical_line(color=WHITE, x_pos=150)
        self.stockSurface.draw_vertical_line(color=WHITE, x_pos=199)
        self.stockSurface.show_display()

    def test_add_image(self):
        image = StockSurface.load_image(path=join(dirname(__file__), 'tree.svg'), size = (50,50))
        self.stockSurface.add_image(image=image, pos=(0,0))
        self.stockSurface.show_display()

    def test_add_text(self):
        self.stockSurface.add_text('HELLO', WHITE, (0,0))
        self.stockSurface.show_display()

    def test_add_multline_text(self):
        multi_lines = [("Multi_line 1", RED), ('Multi_line 2', WHITE)]
        self.stockSurface.add_multline_text(lines=multi_lines, pos=(25,25))
        self.stockSurface.show_display()