import pygame
from os.path import dirname, join
from typing import List, Tuple
from stock_plotter.Helper import Action
from stock_plotter.Helper.Contants import *
from stock_plotter.Helper.Functions import ss
from stock_plotter.Surface import StockSurface


class CatTrader():
    size = 50

    def reset(self, starting_capital:float = 1000.0) -> None:
        #NOTE: Once this is True, this means that the trader is dead. We must not process this,
        # however we can still draw the death statistics!
        self._isDead = False
        self._inTrade = False

        # Trader state values
        assert(starting_capital > 0), "Starting money for CatTrader must be greater than 0"
        self._capital = starting_capital    # Current capital
        self._unrealized_gains = 0.0    # Potential gain/loss for if in trade
        self._trades = 0    # No. of trader done uptil now
        self._cum_losses = 0.0  # Cummulative loss done on all trades
        self._cum_profits = 0.0 # Cummulative Profit done on all trades
        self._holding = 0.0 # No. of coins being held
        self._buy_price = 0.0

    def __init__(self, starting_capital:float = 1000.0, death_at:float = 0.75) -> None:
        # These images can be made class global but they require that pygame be init and setup
        self.alive_cat =  StockSurface.load_image(join(dirname(__file__), "cat.svg"), (self.size, self.size))
        self.dead_cat =  StockSurface.load_image(join(dirname(__file__), "death.svg"), (self.size, self.size))
        # Used by reset to properly setup variables
        self.initial_starting_capital = starting_capital
        self._death_at = self.initial_starting_capital * death_at 
        # Use the reset as intializing point for all the member variables
        self.reset(self.initial_starting_capital)

    def draw(self, stockSurface:StockSurface, x_pos:int):
        assert(x_pos >= 0), "x_pos must be positive"
        y_pos = self._get_y_pos()
        stockSurface.draw_vertical_line(x_pos=x_pos)
        image = self.dead_cat if self.isDead else self.alive_cat
        stockSurface.add_image(image=image, pos = (x_pos - self.size, y_pos))
        # Add the stats 
        stats = self._get_display_stats()
        # Adding some pace between the line and stats
        stockSurface.add_multline_text(lines=stats, pos = (x_pos + 1 , y_pos))

    def _get_y_pos(self) -> int:
        # The y-pos is determined by the starting capital and the current status of the trader
        # We consider that the screen is 3 times the starting capital and the starting capital is 
        # always 1/3
        total_screen = 3 * self.initial_starting_capital
        ratio = (self.current_value + self._unrealized_gains) /total_screen
        return ss(max(min(ratio, 0.9), 0.1))

    def _get_display_stats(self) -> List[Tuple[str, Tuple]]:
        # we compute the stats here as a list of str that can be directly printed
        #print unrealiuzed gains + trades made? -> this needs to be replicating the 
        # input required by StockSurface.add_multiine_text()
        color = GREEN if self._unrealized_gains > 0 else RED
        return [
            (f'Gains: {self._unrealized_gains:0.2f}', color),
            (f'{self.current_value:0.2f}', WHITE),
            (f'Trades: {self._trades}', WHITE)]


    # Useful properties
    @property
    def isDead(self) -> bool:
        return self._isDead

    @property
    def current_capital(self) -> float:
        return self._capital

    @property
    def death_at(self) -> float:
        return self._death_at
    
    @property
    def assets_holding(self) -> float:
        return self._holding
    
    @property
    def cum_profit(self) -> float:
        return self._cum_profits

    @property
    def cum_losses(self) -> float:
        return self._cum_losses

    @property
    def trades_done(self) -> int:
        # Trade will only be done one buy and sell happens
        return self._trades

    @property
    def unrealized_gains(self) -> float:
        # Gains is profit or loss based on the bought price
        return self._unrealized_gains
    
    @property 
    def current_value(self) -> float:
        return (self._holding * self._buy_price) + self._capital

    
    def process(self, action:Action, close:float) -> float:
        # This will change the internal variables values
        assert(close != 0.0), "Close values cannot be 0"
        reward = self._compute_reward(action, close)
        self._update(action, close)
        return reward

    def _update(self, action:Action, close:float) -> None:
        if action == Action.BUY:
            # Only buy when in not trade
            if not self._inTrade:
                self._holding = self._capital / close
                self._capital -= self._holding * close
                self._buy_price = close
                self._inTrade = True
        elif action == Action.HOLD:
            # Only update the unrealized gains if in trade
            if self._inTrade:
                self._unrealized_gains =  (close - self._buy_price) * self._holding
        elif action == Action.SELL:
            # Only sell when already in trade
            if self._inTrade:
                # Determine to add to profit or loss
                pnl = (close - self._buy_price) * self._holding
                if pnl > 0.0:
                    self._cum_profits += pnl
                else:
                    self._cum_losses +=  abs(pnl)

                # Reset the other values
                self._capital += close * self._holding
                self._isDead = True if self._capital < self._death_at else False
                self._holding = 0.0
                self._buy_price = 0.0
                self._unrealized_gains = 0.0
                self._inTrade = False

                #Increment trade
                self._trades += 1

    # Here are the main reward functions
    def _compute_reward(self, action:Action, close:float) -> float:
        reward = None
        if action == Action.BUY:
            reward = 1.0 if not self._inTrade else -1.0
        elif action == Action.HOLD:
            if self._inTrade:
                reward = 0.5 if close > self._buy_price else -0.5
            else:
                reward = -0.1
        elif action == Action.SELL:
            if self._inTrade:
                change_percentage = (close - self._buy_price)/self._buy_price
                reward = 1 + change_percentage if change_percentage > 0.0 else - 2 - change_percentage
            else:
                reward = -1.0
        assert(reward), "NONE reward computed!"
        return reward