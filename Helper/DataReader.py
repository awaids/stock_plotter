import pandas as pd
def read_csv(csv: str, normalize:bool=False) -> pd.DataFrame:
    """ Reads the provided csv and returns a dataframe that is already
        scaled to the maximum price on the data frame """
    df = pd.read_csv(csv)
    max_price = max(df["High"])
    if normalize:
        for col in ['Open', 'Close', 'High', 'Low']:
            df[col] = df[col].div(max_price)
    return df


class StockDataDF:
    """ Class to maniuplate the DataFrame for pygame  """
    _REQUIRED_COLUMNS = {'High', 'Low', 'Close', 'Open'}
    def __init__(self, df:pd.DataFrame) -> None:
        for col in self._REQUIRED_COLUMNS:
            assert(col in df.columns), "Missing column in df"
        self.df:pd.DataFrame = df
        # Normalize the df
        self._Normalizing_factor = self.df['High'].max()
        for col in ['Open', 'Close', 'High', 'Low']:
            self.df[col] = self.df[col].div(self._Normalizing_factor)
    
    def de_normalize(self, val:float) -> float:
        """ Returns the de-normalized value """
        return val * self._Normalizing_factor