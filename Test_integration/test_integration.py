from time import sleep
from stock_plotter.Trader import CatTrader
from os.path import dirname, join
from stock_plotter.Candle import CandleSticks
from stock_plotter.Helper import Action
from stock_plotter.Helper.DataReader import StockDataDF
from stock_plotter.Helper.DataReader import read_csv
from stock_plotter.Surface import StockSurface
from random import seed, randint
seed(1)

def get_action() -> Action:
    return Action.get_action(randint(0,2))


class TestCatTrader_StockDataDF_Integration:
    stockSurface = StockSurface(caption="Integration Test")
    # stockData = StockDataDF(read_csv(join(dirname(__file__), 'BTCUSDT_1d.csv')))
    # stockData = StockDataDF(read_csv(join(dirname(__file__), 'ADAUSDT_1d.csv')))
    
    def test_winning_cat(self):
        trader = CatTrader(starting_capital=100)
        close = 1
        for i in range(0,self.stockSurface.screen_width):
            self.stockSurface.clear_display()
            action = get_action()
            trader.process(action, close)
            trader.draw(stockSurface=self.stockSurface, x_pos=i)
            self.stockSurface.show_display()
            close *= 1.01
    
    
    def test_losing_cat(self):
        trader = CatTrader(starting_capital=100)
        close = 1
        for i in range(0,self.stockSurface.screen_width):
            self.stockSurface.clear_display()
            action = get_action()
            trader.process(action, close)
            trader.draw(stockSurface=self.stockSurface, x_pos=i)
            self.stockSurface.show_display()
            close *= .99

    def _n_traders(self, n:int):
        traders = [CatTrader(starting_capital=100) for _ in range(n)]
        stockData = StockDataDF(read_csv(join(dirname(__file__), 'BTCUSDT_1d.csv'))[:100])
        for df in stockData.df_generator():
            close = stockData.get_last_close(df)
            self.stockSurface.clear_display()
            CandleSticks(df).draw(stockSurface=self.stockSurface)
            for trader in traders:
                # Apply some action
                action = get_action()
                trader.process(action, close)
                trader.draw(stockSurface=self.stockSurface, x_pos=self.stockSurface.last_x_pos)
            self.stockSurface.show_display()
            sleep(0.05)


    def test_onetrader(self):
        self._n_traders(1)

    def test_5trader(self):
        self._n_traders(5)



