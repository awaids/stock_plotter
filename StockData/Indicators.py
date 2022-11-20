import pandas as pd
import numpy as np
import talib as ta
from typing import List
from abc import ABC, abstractmethod
from sklearn.preprocessing import MinMaxScaler

_scaler = MinMaxScaler(feature_range=(0, 1))
def normalize(ap_array:np.ndarray) -> np.ndarray:
    assert(not np.isnan(ap_array).all()), "An array will all NaN recieved for normalization"
    # maintain shape to reset
    return _scaler.fit_transform(ap_array.astype(float).reshape(-1, 1)).reshape(ap_array.shape)


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

    def _compute(self, df:pd.DataFrame):
        close = df['Close'].to_numpy()
        col = self.__class__.__name__
        ema = ta.EMA(close, timeperiod=self.Period)
        df[col] = normalize(ema)


class EMAvsClose(IndicatorBase):
    _Periods = [25,50,100,150]
    Period = max(_Periods)
    Required_Columns = {'Close'}

    def output_cols(self) -> List[str]:
        return [f'ema{period}vsClose' for period in self._Periods]

    def _compute(self, df:pd.DataFrame):
        close = df['Close'].to_numpy()
        for period in self._Periods:
            ema = ta.EMA(close, timeperiod=period)
            df[f'ema{period}vsClose'] = np.where(close > ema, 1.0, 0.0)

        

class RSI14(IndicatorBase):
    Period = 14 + 1 # +1 is required here as 14 we get all NaNs
    Required_Columns = {'Close'}
    def output_cols(self) -> List[str]:
        return ['RSI14']

    def _compute(self, df:pd.DataFrame):
        close = df['Close'].to_numpy()
        col = 'RSI14'
        # Substract 1 from the period as we still to get the last value
        df[col] = ta.RSI(close, timeperiod=self.Period - 1) / 100


class BB24(IndicatorBase):
    # I dont like this one, as this once normalizes will not make any sense as BB bands are always 2 STD above and below!
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
        u, m, l = normalize(np.vstack((u,m,l)))

        # Assigning to df
        df[f'{self.__class__.__name__}Lower'] = l
        df[f'{self.__class__.__name__}Middle'] = m
        df[f'{self.__class__.__name__}Upper'] = u


class BB24Squeeze(IndicatorBase):
    # Indicator to determine the current squeeze of the BBband
    Period = 24
    Required_Columns = {'Close'}
    def output_cols(self) -> List[str]:
        return ['BB24Squeeze']

    def _compute(self, df:pd.DataFrame):
        close = df['Close'].to_numpy()
        u, _, l = ta.BBANDS(close, timeperiod=self.Period, nbdevup=2, nbdevdn=2, matype=0)
        df['BB24Squeeze'] = normalize(u - l)


class PctChange_Scaler(IndicatorBase):
    """ Base class for pct change and scaling between 0.0 - 1.0 """
    Period = 2  # Period required here is 3. Once for pct change and one for normalization
    def _compute(self, df:pd.DataFrame):
        for col in self.Required_Columns:
            new_col = df[col].pct_change()
            df[f'{col}_v2'] = normalize(new_col.to_numpy())
    
    def output_cols(self) -> List[str]:
        """ Returns a list of cols that this indicator will append to the df """
        return [f'{col}_v2' for col in self.Required_Columns]


class CLOSE_v2(PctChange_Scaler):
    Required_Columns = {'Close'}