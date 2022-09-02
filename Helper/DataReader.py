from __future__ import annotations
from abc import ABC, abstractmethod, abstractstaticmethod
import os
import pandas as pd
import talib as TA
import numpy as np
from math import log10, ceil


def read_csv(csv: os.PathLike, normalize:bool=False) -> pd.DataFrame:
    """ Reads the provided csv and returns a dataframe that is already
        scaled to the maximum price on the data frame """
    df = pd.read_csv(csv)
    max_price = max(df["High"])
    if normalize:
        for col in ['Open', 'Close', 'High', 'Low']:
            df[col] = df[col].div(max_price)
    return df


# class NeatDataBase(ABC):
#     def __init__(self, df: pd.DataFrame) -> None:
#         required_columns = {'Close', 'Open',
#                             'High', 'Low', 'Volume', 'CloseTime'}
#         assert(not required_columns.difference(set(df.columns))
#                ), 'Required columns misisng in df!'
#         self.df = df

#     @abstractmethod
#     def get_neat_input(self, index: int) -> np.array:
#         """ This function should return the observation space for the provided index, here manipualtion can be done on the pd.Series """
#         return self.df.iloc[index].to_numpy()

#     def get_input_node_names(self) -> dict:
#         pass


# class BinaryFeaturesDataset(NeatDataBase):
#     PERIODS = [5, 10, 20, 50, 100, 200]

#     def __init__(self, csvFile: os.PathLike) -> None:
#         # Setup the base with df
#         df = pd.read_csv(csvFile)
#         super().__init__(df)

#         # Compute the df with binary feature
#         bool2floatDict = {True: 1.0, False: 0.0}

#         # Compute indicators for time periods
#         for ref in ['Close', 'Volume']:
#             ref_series = self.df[ref]
#             for period in self.PERIODS:
#                 self.df[f'EMA_{ref}_{period}'] = TA.EMA(
#                     ref_series, timeperiod=period)

#             # Add Gradients for the EMAs
#             for period in self.PERIODS:
#                 ema = self.df[f'EMA_{ref}_{period}']
#                 self.df[f'Grad_{ref}_{period}'] = ema.diff(
#                     periods=1).div(ema).mul(100)

#             # Determine ema cross
#             for idx1, period1 in enumerate(self.PERIODS):
#                 for period2 in self.PERIODS[idx1+1:]:
#                     p1 = self.df[f'EMA_{ref}_{period1}']
#                     p2 = self.df[f'EMA_{ref}_{period2}']
#                     self.df[f'Feature_EMAcross_{ref}_{period1}_{period2}'] = p1.gt(
#                         p2).replace(bool2floatDict)

#             # Determine gradients diff
#             for period in self.PERIODS:
#                 grad_diff = self.df[f'Grad_{ref}_{period}'].diff(periods=1)
#                 self.df[f'Feature_GradDiff_{ref}_{period}'] = grad_diff.apply(
#                     lambda x: 0.0 if x <= 0.0 else 1.0)

#         # Bollinger band crosses for the close only
#         for period in self.PERIODS:
#             close = self.df['Close']
#             bbu, _, bbd = TA.BBANDS(
#                 close, timeperiod=period, nbdevup=2, nbdevdn=2, matype=0)
#             self.df[f'Feature_BBU{period}_cross'] = close.gt(
#                 bbu).replace(bool2floatDict)
#             self.df[f'Feature_BBD{period}_cross'] = close.lt(
#                 bbd).replace(bool2floatDict)

#         # Clear up the NA and reindex after dropping
#         self.df.dropna(inplace=True)
#         self.df.reset_index(inplace=True)

#         self.colsToRemove = [
#             col for col in self.df.columns if not col.startswith('Feature')]
#         self.sortedFeatureCol = sorted(
#             list(set(self.df.columns).difference(set(self.colsToRemove))))
#         # print(self.df.head())

#     def get_neat_input(self, index: int) -> np.array:
#         series = self.df.iloc[index]
#         return series.drop(columns=self.colsToRemove).reindex(self.sortedFeatureCol).to_numpy()

#     def get_input_node_names(self) -> dict:
#         bin_features_len = len(self.sortedFeatureCol) + 1
#         node_names = dict()
#         for idx, feature in zip(range(-1, -bin_features_len, -1), self.sortedFeatureCol):
#             node_names[idx] = feature
#         node_names[-bin_features_len] = 'InOrder'
#         return node_names

# class OHCLDataset(NeatDataBase):
#     def __init__(self, csvFile: os.PathLike) -> None:
#         super().__init__(pd.read_csv(csvFile))
#         order = ceil(log10(max(self.df['High'])))  # + 1
#         self._max_price = 10**order
#         for col in ['Open', 'Close', 'High', 'Low']:
#             self.df[f'Normalized_{col}'] = self.df[col].div(self._max_price)

#         self.colsToRemove = [
#             col for col in self.df.columns if not col.startswith('Normalized')]
#         self.sortedFeatureCol = sorted(
#             list(set(self.df.columns).difference(set(self.colsToRemove))))

#     def get_neat_input(self, index: int) -> np.array:
#         series = self.df.iloc[index]
#         return series.drop(columns=self.colsToRemove).reindex(self.sortedFeatureCol).to_numpy()
