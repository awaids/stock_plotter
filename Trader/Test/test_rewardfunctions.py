import pytest
from stock_plotter.Trader.RewardFunction import *

class Test_reward_winning_trades:
    def test_holds(self):
        # Holding when not in trade
        temp, final = reward_winning_trades(Action.HOLD, close=10, inTrade=False, buyPrice=None)
        assert(temp == WRONG_ACTION)
        assert(final == 0)
        # Holding with price rising
        temp, final = reward_winning_trades(Action.HOLD, close=10, inTrade=True, buyPrice=5)
        assert(temp == RIGHT_ACTION)
        assert(final == 0)
        # Holding with proce losing
        temp, final = reward_winning_trades(Action.HOLD, close=10, inTrade=True, buyPrice=15)
        assert(temp == WRONG_ACTION)
        assert(final == 0)

    def test_buys(self):
        # Buying when in trader
        temp, final = reward_winning_trades(Action.BUY, close=10, inTrade=True, buyPrice=5)
        assert(temp == WRONG_ACTION)
        assert(final == 0)
        # Buying from scratch
        temp, final = reward_winning_trades(Action.BUY, close=10, inTrade=False, buyPrice=None)
        assert(temp == RIGHT_ACTION)
        assert(final == 0)

    def test_sells(self):
        # Selling when not in trade
        temp, final = reward_winning_trades(Action.SELL, close=10, inTrade=False, buyPrice=None)
        assert(temp == WRONG_ACTION)
        assert(final == 0)
        # Selling with loss
        temp, final = reward_winning_trades(Action.SELL, close=10, inTrade=True, buyPrice=20)
        assert(temp == 0)
        assert(final == -4.5)
        # Selling with profit
        temp, final = reward_winning_trades(Action.SELL, close=10, inTrade=True, buyPrice=8)
        assert(temp == 0)
        assert(final == 2.25)
        # Selling with profit capped
        temp, final = reward_winning_trades(Action.SELL, close=10, inTrade=True, buyPrice=2)
        assert(temp == 0)
        assert(final == 3.0)
