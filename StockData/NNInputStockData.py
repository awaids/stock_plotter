from __future__ import annotations
from pathlib import Path
from queue import Empty
from .Indicators import IndicatorBase
from typing import Set, List
import pandas as pd
import numpy as np
import pickle

class NNInputStockData:
    ''' This class is used to manipulte the basic stock dataframe such that it can be feed as input
        to a NN for both training and inference '''
    Base_Columns = {'Open', 'Close', 'High', 'Low'}

    def __init__(self, historical_period:int=100) -> None:
        # Historical period means hows many older klines to ensure that some historical data is accounted for
        # when normalizhing and scaling
        self._indicators: Set[IndicatorBase] = set()
        self._historical_period = historical_period

    def register_indicator(self, indicator:IndicatorBase) -> None:
        self._indicators.add(indicator)

    def register_indicators(self, indicators:List[IndicatorBase]) -> None:
        for ind in indicators:
            self.register_indicator(ind)

    def get_indicators_period(self) -> int:
        if not self._indicators:
            return 1
        return max([ind.Period for ind in self._indicators])

    @property
    def required_period(self) -> int:
        # Required period for indicators and historical data to normalize aganist
        return self.get_indicators_period() + self._historical_period

    @property
    def required_cols(self) -> Set[str]:
        cols = self.Base_Columns
        for ind in self._indicators:
            cols = cols | ind.Required_Columns
        return cols

    @property
    def output_cols(self) -> List[str]:
        """ Sorted list of all the columns that the output will contain """
        cols = list(self.Base_Columns)
        for ind in self._indicators:
            cols = cols + ind().output_cols()
        return sorted(cols)

    def add_indicators_to_df(self, df:pd.DataFrame):
        # Adds columns for the indicators to the current df
        for ind in self._indicators:
            ind().add_indicator_col(df=df)

    def prepare_input(self, df:pd.DataFrame) -> np.ndarray:
        """ Prepares the df with appending the indicators info and also returns
            a single observation """
        # Asserts to ensure that the df can consume the df
        assert(self.required_cols.issubset(df.columns)), "Columns required by indicators not in df"
        assert(df.shape[0] >= self.required_period + 1), "Dataframe size is less than max period of indicators"

        # Truncate the df to make processing slighlty less cumbersome
        new_df = df.iloc[-(self.required_period+1):].copy(deep=True)
        # Drop all columns that are not base columns
        new_df.drop(columns=new_df.columns.difference(self.Base_Columns), inplace=True)
        # Add the indicators values
        self.add_indicators_to_df(new_df)
        for col in self.Base_Columns:
            new_df[col] = new_df[col].pct_change()
        
        # Sort the columns by name else we might get different orders!
        new_df = new_df.reindex(sorted(new_df.columns), axis=1)
        return new_df.iloc[-1].to_numpy()

    def dump(self, file:Path) -> None:
        """ Dumps the class object to file so it can be later used """
        with open(file, 'wb') as fp:
            pickle.dump(self, fp, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, pkl_file:Path) -> NNInputStockData:
        """ Loads and returns an object of the class from file """
        with open(pkl_file, 'rb') as inp:
            obj = pickle.load(inp)
        return obj