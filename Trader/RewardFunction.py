from typing import Tuple
from stock_plotter.Helper import Action

# List of rewards
WRONG_ACTION = -1.0
RIGHT_ACTION = 0.5
WON_TRADE = 2.0
LOST_TRADE = -4.0

def reward_winning_trades(action:Action, close:float, inTrade:bool, buyPrice:float=None) -> Tuple[float, float]:
    """ Function to reward winning trades and penalize losing trades.
        Also uses the temp and final reward scheme to mck delayed rewards
        Caps the wining rewards"""
    rewardTemp, rewardFinal = 0, 0
    if action == Action.BUY:
        if inTrade:
            rewardTemp = WRONG_ACTION
        else:
            rewardTemp = RIGHT_ACTION
    elif action == Action.HOLD:
        if inTrade and (close > buyPrice):
            rewardTemp = RIGHT_ACTION
        else:
            rewardTemp = WRONG_ACTION
    elif action == Action.SELL:
        if inTrade:
            change_percentage = (close - buyPrice)/buyPrice
            # Reward with change percent
            if change_percentage > 0.0:
                rewardFinal = WON_TRADE + min(1.0, change_percentage)
            else:
                rewardFinal = LOST_TRADE + change_percentage
        else:
            rewardTemp = WRONG_ACTION
    return rewardTemp, rewardFinal

# def _compute_reward(self, action:Action, close:float) -> Tuple[float, float]:
#         rewardTemp, rewardFinal = 0, 0
#         if action == Action.BUY:
#             rewardTemp = 1.0 if not self._inTrade else -1.0
#         elif action == Action.HOLD:
#             if self._inTrade:
#                 rewardTemp = 0.5 if close > self._buy_price else -0.5
#             else:
#                 rewardTemp = -0.1
#         elif action == Action.SELL:
#             if self._inTrade:
#                 change_percentage = (close - self._buy_price)/self._buy_price
#                 rewardFinal = 1 + change_percentage if change_percentage > 0.0 else - 2 - change_percentage
#             else:
#                 rewardFinal = -1.0
#         assert(rewardTemp), "NONE reward computed!"
#         return rewardTemp, rewardFinal