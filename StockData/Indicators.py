import pandas as pd
import numpy as np
import talib as ta
from typing import List
from abc import ABC, abstractmethod

def normalize(ap_array:np.ndarray, minV:float=None, maxV:float=None) -> np.ndarray:
    if minV is None:
        minV = np.nanmin(ap_array)
    if maxV is None:
        maxV = np.nanmax(ap_array)
    # Scale between 0 - 1
    return (ap_array - minV) / (maxV - minV)

class IndicatorBase(ABC):
    ''' Required base class for indicators. This will ensure that we can easily add indicators
        to DF for input to NN '''
    Required_Columns = {'Open', 'Close', 'High', 'Low'}
    Period = None

    def __init__(self) -> None:
        super().__init__()
        assert(self.Period > 0), "Period must be greater than 1"

    @abstractmethod
    def _compute(self, df:pd.DataFrame):
        raise NotImplementedError
    
    @abstractmethod
    def output_cols(self) -> List[str]:
        """ Returns a list of cols that this indicator will append to the df """
        raise NotImplementedError

    def add_indicator_col(self, df:pd.DataFrame):
        # This function will update the current df -> otherwise this might
        # become very slow!
        assert(self.Required_Columns.issubset(df.columns)), "Required cols not in DF"
        assert(df.shape[0] >= self.Period), "DF size is not upto required period"
        return self._compute(df)


class EMA50(IndicatorBase):
    Period = 50
    Required_Columns = {'Close'}
    def output_cols(self) -> List[str]:
        return [self.__class__.__name__]

    def _compute(self, df:pd.DataFrame) -> pd.DataFrame:
        close = df['Close'].to_numpy()
        col = self.__class__.__name__
        ema = ta.EMA(close, timeperiod=self.Period)
        df[col] = normalize(ema)
    

class BB24(IndicatorBase):
    Period = 24
    Required_Columns = {'Close'}
    def output_cols(self) -> List[str]:
        return [
            f'{self.__class__.__name__}Lower',
            f'{self.__class__.__name__}Middle',
            f'{self.__class__.__name__}Upper'
        ]

    def _compute(self, df:pd.DataFrame):
        close = df['Close'].to_numpy()
        u, m, l = ta.BBANDS(close, timeperiod=self.Period, nbdevup=2, nbdevdn=2, matype=0)
        # Normlaizing them differently
        maxV = max([np.nanmax(a) for a in [u,m,l]])
        minV = min([np.nanmin(a) for a in [u,m,l]])

        # Assigning to df
        df[f'{self.__class__.__name__}Lower'] = normalize(l, minV=minV, maxV=maxV)
        df[f'{self.__class__.__name__}Middle'] = normalize(m, minV=minV, maxV=maxV)
        df[f'{self.__class__.__name__}Upper'] = normalize(u, minV=minV, maxV=maxV)