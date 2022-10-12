from .DataReader import StockDataDF
from abc import ABC, abstractstaticmethod
from typing import Set, List
import pandas as pd
import numpy as np
import talib 


class IndicatorBase(ABC):
    @abstractstaticmethod
    def get_period() -> int:
        raise NotImplementedError
    
    @abstractstaticmethod
    def add_indicator_col(df:pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

class NNInputStockData:
    ''' This class is used to manipulte the basic stock dataframe such that it can be feed as input
        to a NN for both training and inference '''
    def __init__(self) -> None:
        self._indicators: Set[IndicatorBase] = set()

    def register_indicator(self, indicator:IndicatorBase) -> None:
        self._indicators.add(indicator)

    def register_indicators(self, indicators:List[IndicatorBase]) -> None:
        for ind in indicators:
            self.register_indicator(ind)

    @property
    def period(self) -> int:
        # Retruns the max time period required for all indicator
        return max([ind.get_period() for ind in self._indicators])

    def add_indicators_to_df(self, df:pd.DataFrame) -> pd.DataFrame:
        assert({'High', 'Low', 'Close', 'Open'}.issubset(df.columns))
        # Adds columns for the indicators
        for ind in self._indicators:
            ind.add_indicator_col(df)
        return df
    