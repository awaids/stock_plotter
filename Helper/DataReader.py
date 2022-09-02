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