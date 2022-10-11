from stock_plotter.Helper import Action

def calculate_reward(action:Action, close:float, buyPrice:float=None) -> float:
    pass
        # reward = 0
        # if action == Action.BUY:
        #     reward = 1.0 if not self._inTrade else -1.0
        # elif action == Action.HOLD:
        #     if self._inTrade:
        #         reward = 0.01 if close > self._buy_price else -0.01
        #     else:
        #         reward = -0.5
        # elif action == Action.SELL:
        #     if self._inTrade:
        #         change_percentage = (close - self._buy_price)/self._buy_price
        #         reward = 2 if change_percentage > 0.0 else -2
        #     else:
        #         reward = -1.0
        # return reward