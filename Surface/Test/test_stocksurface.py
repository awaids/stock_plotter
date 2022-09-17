from os.path import join, dirname
from stock_plotter.Surface import StockSurface
from stock_plotter.Helper.Contants import *

class TestStockSurface:
    local_surface = StockSurface(caption="Test", x_size=200, y_size=100)

    def test_screen_dim(self):
        pygame.display.set_mode((200,100))
        assert(self.local_surface.screen_height == 100), "Height not correct"
        assert(self.local_surface.screen_width == 200), "Width not correct"

    def test_draw_line(self):
        self.local_surface.draw_line(color=WHITE, start=(0,0),end=(200,100))
        self.local_surface.show_display()

    def test_draw_vertical_line(self):
        self.local_surface.draw_vertical_line(color=WHITE, x_pos=1)
        self.local_surface.draw_vertical_line(color=WHITE, x_pos=150)
        self.local_surface.draw_vertical_line(color=WHITE, x_pos=199)
        self.local_surface.show_display()

    def test_add_image(self):
        image = StockSurface.load_image(path=join(dirname(__file__), 'tree.svg'), size = (50,50))
        self.local_surface.add_image(image=image, pos=(0,0))
        self.local_surface.show_display()

    def test_add_text(self):
        self.local_surface.add_text('HELLO', WHITE, (0,0), False)
        self.local_surface.show_display()

    def test_add_multline_text(self):
        multi_lines = [("Multi_line 1", RED), ('Multi_line 2', WHITE)]
        self.local_surface.add_multline_text(lines=multi_lines, pos=(25,25))
        self.local_surface.show_display()