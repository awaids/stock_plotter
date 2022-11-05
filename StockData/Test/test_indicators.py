from pathlib import Path
from stock_plotter.StockData.Indicators import RSI14
from stock_plotter.StockData.DataReader import read_csv

def test_rsi():
    df = read_csv(Path(__file__).parent / 'BTCUSDT_1d.csv')
    RSI14().add_indicator_col(df=df)
    assert('RSI14' in df.columns)
    assert(df['RSI14'].max() <= 1.0)

