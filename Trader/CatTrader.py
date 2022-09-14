import pygame
from os.path import dirname, join
from stock_plotter.Helper import DrawBase
from stock_plotter.Helper import Action


class CatTrader(DrawBase):
    def __init__(self, starting_capital:float = 1000.0) -> None:
        #TODO: figure out how to make the image here universal! -> needs pygame init
        image = pygame.image.load(join(dirname(__file__), "TraderCat.png")).convert()
        self.image = pygame.transform.scale(image, (50, 50))
        # Used by reset to properly setup variables
        self.initial_starting_capital = starting_capital
        # Use the reset as intializing point for all the member variables
        self.reset(self.initial_starting_capital)

    def draw(self, parent_surface: pygame.Surface) -> pygame.Surface:
        parent_surface.blit(self.image, (0,0))
        return parent_surface

    def reset(self, starting_capital:float = 1000.0) -> None:
      # Once this is false, this means that the trader is dead. We must not process this,
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

    # Useful properties
    @property
    def isDead(self) -> bool:
        return self._isDead

    @property
    def current_capital(self) -> float:
        return self._capital
    
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
        return self._unrealized_gains
    
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