import pandas as pd

def read_csv(csv: str) -> pd.DataFrame:
    """ Reads the provided csv and returns a dataframe"""
    required_coulmns = {'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
       'QuoteAssetVol', 'NumberTrades', 'BuyBaseAssetVol', 'BuyQuoteAssetVol'}
    df = pd.read_csv(csv)
    assert(required_coulmns.issubset(set(df.columns))), "Requierd columns not found in Dataframe"
    return df


class StockDataDF:
    """ Class to maniuplate the DataFrame for pygame  """
    _REQUIRED_COLUMNS = {'High', 'Low', 'Close', 'Open'}
    def __init__(self, df:pd.DataFrame) -> None:
        for col in self._REQUIRED_COLUMNS:
            assert(col in df.columns), "Missing column in df"
        self._df:pd.DataFrame = df
        # Normalize the df
        self._Normalizing_factor = self._df['High'].max()
        for col in ['Open', 'Close', 'High', 'Low']:
            self._df[col] = self._df[col].div(self._Normalizing_factor)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def num_entries(self) -> int:
        return self._df.shape[0]

    def live_generator(self,):
        for idx in range(1, self.num_entries):
            yield self._df[:idx]

    def de_normalize(self, val:float) -> float:
        """ Returns the de-normalized value """
        return val * self._Normalizing_factor