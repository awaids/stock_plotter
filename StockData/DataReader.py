from pathlib import Path
import pandas as pd
from typing import List

def read_csv(csv: Path) -> pd.DataFrame:
    """ Reads the provided csv and returns a dataframe"""
    assert(Path.exists(csv))
    required_coulmns = {'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
       'QuoteAssetVol', 'NumberTrades', 'BuyBaseAssetVol', 'BuyQuoteAssetVol'}
    df = pd.read_csv(csv)
    assert(required_coulmns.issubset(set(df.columns))), "Requierd columns not found in Dataframe"
    return df

class StockDataDF:
    """ Class to maniuplate the DataFrame for pygame  
    NOTE: This class will normalize the values!"""
    _REQUIRED_COLUMNS = ['High', 'Low', 'Close', 'Open']
    def __init__(self, df:pd.DataFrame, normalize:bool=True) -> None:
        for col in self._REQUIRED_COLUMNS:
            assert(col in df.columns), "Missing column in df"
        
        # Manipualte the df & drop unnecessary columns
        self._df:pd.DataFrame = df
        
        self._df.drop(columns=self._df.columns.difference(self._REQUIRED_COLUMNS), inplace=True)

        # Normalize the df
        self._Normalizing_factor = self._df['High'].max() if normalize else 1.0
        for col in ['Open', 'Close', 'High', 'Low']:
            self._df[col] = self._df[col].div(self._Normalizing_factor)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def num_entries(self) -> int:
        # Total data in the current dataframe
        return self._df.shape[0]
    
    def get_col_names(self) -> List[str]:
        return self._df.columns

    def df_generator(self) :
        # Only to be used to get live data like df
        # i.e with each iteration returns a growing df
        for idx in range(1, self.num_entries + 1):
            yield self._df[:idx]

    def de_normalize(self, val:float) -> float:
        """ Returns the de-normalized value """
        return val * self._Normalizing_factor

    def get_last_close(self, df:pd.DataFrame) -> float:
        """ Use this function to return the denormalized close value
        NOTE: this must be always use when sending it to the trader
        as clsoe value """
        assert(df.shape[0] >= 1), "Empty df has been received"
        return self.de_normalize(df.iloc[-1]['Close'])
