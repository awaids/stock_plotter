import pytest
import numpy as np
from pathlib import Path
from stock_plotter.StockData.Indicators import RSI14, CLOSE_v2, BB24, BB24Squeeze, EMAvsClose, normalize
from stock_plotter.StockData.DataReader import read_csv

def test_CLOSE_v2_ind():
    df = read_csv(Path(__file__).parent / 'BTCUSDT_1d.csv')[:4]
    CLOSE_v2().add_indicator_col(df=df)
    ind = df['Close_v2'].to_numpy()
    ref = np.array([np.nan, 0.0, 1.0, 0.39792918])
    assert(np.allclose(ind, ref, equal_nan=True)), "CLOSE_v2 ind values not correct"

def test_RSI4():
    df = read_csv(Path(__file__).parent / 'BTCUSDT_1d.csv')[:15]
    with pytest.raises(AssertionError):
        # This should fail as we need 15 period
        RSI14().add_indicator_col(df[:14])
    
    RSI14().add_indicator_col(df)
    rsi14 = df['RSI14'].to_numpy()
    assert(np.isclose(rsi14[-1],0.4121504347)), "The RSI14 values didnt match"

def test_BB24():
    df = read_csv(Path(__file__).parent / 'BTCUSDT_1d.csv')[:24]
    BB24().add_indicator_col(df)
    obs = [df[col].iloc[-1] for col in BB24().output_cols()]
    ref = [0, 0.5, 1.0]
    assert(np.allclose(obs, ref))

def test_BB24Squeeze():
    df = read_csv(Path(__file__).parent / 'BTCUSDT_1d.csv')[100:129]
    BB24Squeeze().add_indicator_col(df)
    assert(df['BB24Squeeze'].to_numpy()[-1] == 0.0)


class TestNormalize():
    def test_normalize(self):
        series = np.array([90, 91, 85, 99.0])
        series = normalize(series)
        ref = np.array([0.357143, 0.428571, 0.0, 1.0])
        assert(np.isclose(series, ref, equal_nan=True).all())
    
    def test_assertions(self):
        # Check if single element can be normalized
        obs = normalize(np.array([35]))
        ref = np.array([0.0], dtype=float)
        assert((ref == obs).all())

        # Check if min max elemenets work
        obs = normalize(np.array([35, 36]))
        ref = np.array([0.0, 1.], dtype=float)
        assert((ref == obs).all())
        
        # Check if same element can be normalized
        obs = normalize(np.array([35, 35]))
        ref = np.array([0.0, 0.0], dtype=float)
        assert(np.allclose(ref, obs))

        # Check for multi row numpy array (Similar to what we would get from talib)
        r1 = np.array([25.0, 50.0, 60.0], dtype=float)
        r2 = np.array([2.05, 0.0, 1.0], dtype=float)
        r = np.vstack((r1, r2))
        ref = np.array([[0.41666667, 0.83333333, 1.0], [0.03416667, 0.0, 0.01666667]], dtype=float)
        obs = normalize(r)
        assert(np.allclose(obs, ref)), "Multi row reference not same"

        # check normalize with NaN
        r = np.array([np.nan, 0.0, 0.5, 1.5])
        obs = normalize(r)
        ref = np.array([np.nan, 0.0, 0.33333333, 1.0])
        assert(np.allclose(ref, obs, equal_nan=True)), "NaN array assert failed"

        # check normalize with negative values
        r = np.array([-0.5, 0.0, 0.5, 1.5])
        obs = normalize(r)
        ref = np.array([0.0, 0.25, 0.5,  1.0])
        assert(np.allclose(ref, obs, equal_nan=True)), "Negative values array assert failed"

        # Check all NaN assertion
        with pytest.raises(AssertionError):
            normalize(np.array([np.nan, np.nan]))
