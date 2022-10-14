import pytest
from stock_plotter.Helper.Bases import Action
from stock_plotter.Trader import CatTrader
from stock_plotter.Helper.Functions import setup_disply

class CatTrderWrapper(CatTrader):
    def __init__(self, starting_capital: float = 1000, death_at: float = 0.75) -> None:
        super().__init__(starting_capital, death_at)
    
    def get_internals(self) -> list:
        # Returns the values of the CatTrader variables
        return [
            self.current_capital,
            self.assets_holding,
            self.unrealized_gains,
            self.cum_profit,
            self.cum_losses,
            self.trades_done,
            self.isDead
        ]


class TestCatTrader:
    setup_disply()
    Trader = CatTrader(starting_capital=100)
    
    def get_internals(self) -> list:
        # Returns the values of the CatTrader variables
        trader = self.Trader
        return [
            trader.current_capital,
            trader.assets_holding,
            trader.unrealized_gains,
            trader.cum_profit,
            trader.cum_losses,
            trader.trades_done,
            trader.isDead
        ]

    def test_process_zero_close_assert(self):
        with pytest.raises(AssertionError):
            self.Trader.process(action=Action.BUY, close=0)

    def test_process_default(self):
        self.Trader.reset()
        assert(self.get_internals() == [100.0, 0.0, 0.0, 0.0, 0.0, 0, False])

    def test_process_trade_buy_sell_profit(self):
        self.Trader.reset()

        # Buy
        self.Trader.process(action=Action.BUY, close=10.0)
        assert(self.get_internals() == [0.0, 10.0, 0.0, 0.0, 0.0, 0, False])

        # Sell with profit
        self.Trader.process(action=Action.SELL, close=20.0)
        print(self.get_internals())
        print(f'Capital : {self.Trader.current_capital}')
        print(f'Death at : {self.Trader.death_at}')
        assert(self.get_internals() == [200.0, 0.0, 0.0, 100.0, 0.0, 1, False])

    def test_process_trade_buy_sell_loss(self):
        self.Trader.reset()
        # Buy
        self.Trader.process(action=Action.BUY, close=10.0)
        assert(self.get_internals() == [0.0, 10.0, 0.0, 0.0, 0.0, 0, False])

        # Sell with loss
        self.Trader.process(action=Action.SELL, close=5.0)
        assert(self.get_internals() == [50.0, 0.0, 0.0, 0.0, 50.0, 1, True])

    def test_process_hold_cases(self):
        self.Trader.reset()

        # Hold with nothing
        self.Trader.update_state(action=Action.HOLD, close=20.0)
        assert(self.get_internals() == [100.0, 0.0, 0.0, 0.0, 0.0, 0, False])

        # Buy
        self.Trader.update_state(action=Action.BUY, close=10.0)

        # Hold with unrealized gains
        self.Trader.update_state(action=Action.HOLD, close=20.0)
        assert(self.get_internals() == [0.0, 10.0, 100.0, 0.0, 0.0, 0, False])

        # Hold with unrealized losses
        self.Trader.update_state(action=Action.HOLD, close=9.0)
        assert(self.get_internals() == [0.0, 10.0, -10.0, 0.0, 0.0, 0, False])

        # Sell with profit
        self.Trader.update_state(action=Action.SELL, close=20.0)

        # Hold with some profit
        self.Trader.update_state(action=Action.HOLD, close=25.0)
        assert(self.get_internals() == [200.0, 0.0, 0.0, 100.0, 0.0, 1, False])
    
    def test_process_multiple_trades(self):
        self.Trader.reset()
        # Buy & sell
        self.Trader.process(action=Action.BUY, close=10.0)
        self.Trader.process(action=Action.SELL, close=20.0)
        self.Trader.process(action=Action.BUY, close=20.0)
        self.Trader.process(action=Action.SELL, close=10.0)
        assert(self.get_internals() == [100.0, 0.0, 0.0, 100.0, 100.0, 2, False])


    def test_display_stats(self):
        self.Trader.reset()
        assert(self.Trader.current_value == 100)

        self.Trader.update_state(action=Action.BUY, close=10.0)
        assert(self.Trader.current_value == 100)

        self.Trader.update_state(action=Action.HOLD, close=15.0)
        assert(self.Trader.current_value == 100)

        self.Trader.update_state(action=Action.HOLD, close=5.0)
        assert(self.Trader.current_value == 100)

        self.Trader.update_state(action=Action.SELL, close=20.0)
        assert(self.Trader.current_value == 100)