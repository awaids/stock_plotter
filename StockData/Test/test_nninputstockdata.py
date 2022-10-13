import pathlib 
import pytest
import pandas as pd
import numpy as np
from stock_plotter.StockData.DataReader import read_csv
from stock_plotter.StockData.DataReader import StockDataDF
from stock_plotter.StockData import IndicatorBase
from stock_plotter.StockData import EMA50, BB24
from stock_plotter.StockData import NNInputStockData
from stock_plotter.StockData.Indicators import normalize


TestDF = read_csv(csv = pathlib.Path(__file__).parent / 'test_data.csv')

def test_normalize():
    series = pd.Series([90, 91, 85, 99])
    series = normalize(series)
    ref = np.array([0.357143,0.428571,0,1])
    assert(np.isclose(series.to_numpy(), ref, equal_nan=True).all())


class Dummy1(IndicatorBase):
    Required_Columns = {'Close'}
    Period = 1
    def _compute(self, df:pd.DataFrame):
        df[__class__.__name__] = df['Close'] * 0.5
        return df

class Dummy2(IndicatorBase):
    Required_Columns = {'Dummy'}
    Period = 5 
    def _compute(self, df:pd.DataFrame):
        return df

class TestIndicators:
    df = TestDF.copy(deep=True)
    def test_indicator_add_col(self):
        ind = Dummy1()
        df = ind.add_indicator_col(self.df)
        assert('Dummy1' in df.columns), "A new column should should be added"
        
    def test_indicator_require_period_assertion(self):
        with pytest.raises(AssertionError):
            Dummy2().add_indicator_col(self.df)

class TestIndicatorEMA50:
    df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
    def test_basic_working_for_perfect_size(self):
        # Test if the indicator value is properly added to a df of perfect size
        df = self.df.iloc[:51].copy()
        EMA50().add_indicator_col(df)
        assert('EMA50' in df.columns), "EMA50 must be in columns"
        assert(np.isclose(df['EMA50'].to_numpy()[-1],1.0)), "The EMA value is not the same"
    
    def test_basic_working_for_bigger_size(self):
        # Test if the indicator value is properly added to a df of size bigger than required
        df = self.df.iloc[-60:].copy()
        EMA50().add_indicator_col(df)
        assert('EMA50' in df.columns), "EMA50 must be in columns"
        assert(np.isclose(df['EMA50'].to_numpy()[-1],1.0)), "The EMA value is not the same"

class TestIndicatorBB24:
    df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv').iloc[:25]
    def test_basic_working(self):
        BB24().add_indicator_col(self.df)
        assert({'BB24Lower', 'BB24Middle', 'BB24Upper'}.issubset(self.df.columns)), "BB24 columns missing"

class TestNNInputStockData:
    df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
    def test_get_period(self):
        # Check if the max period is correctly picked up
        StockData = NNInputStockData()
        StockData.register_indicators(indicators=[BB24, EMA50])
        assert(StockData.get_indicators_period() == 50), "Period must be the max period of all indicators"
    
    def test_get_columns(self):
        # Check if the cols required by indicators are correctly picked up
        StockData = NNInputStockData()
        StockData.register_indicators(indicators=[Dummy1, Dummy2])
        print(f'Cols: {StockData.required_cols}')
        assert(StockData.required_cols == set(['Dummy', 'Close', 'Open', 'Low', 'High'])), "Period must be the max period of all indicators"

    def test_df_period_assertion(self):
        ''' Test assertion when the df is not big enough'''
        df = self.df.copy().iloc[:30]
        StockData = NNInputStockData()
        StockData.register_indicators([BB24, EMA50])
        with pytest.raises(AssertionError):
            StockData.add_indicators_to_df(df)

    def test_df_required_cols_assertion(self):
        ''' Test assertion when the df is not big enough'''
        df = self.df.copy()
        StockData = NNInputStockData()
        StockData.register_indicators([Dummy1, Dummy2])
        with pytest.raises(AssertionError):
            StockData.add_indicators_to_df(df)
    
    def test_prepare_input(self):
        # Tests the complete input preparation by the class
        StockData = NNInputStockData()
        StockData.register_indicators([BB24, EMA50])
        df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
        observation = StockData.prepare_input(df)
        ref = [0.43944644, 0.54003719, 0.64062794, -0.0170059, 0.64087909, -0.10542347, 0.03662134, -0.11008256]
        assert(np.allclose(observation, ref))
    
    def test_pickle_dump_and_load(self):
        ''' Testing if we can dump the NNInputStockData object and re-use it again '''
        df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
        StockData = NNInputStockData()
        StockData.register_indicators([Dummy1])
        ref1 = StockData.prepare_input(df)
        # dump
        StockData.dump(file=pathlib.Path('NNInputStockData.pkl'))
        # load
        obj = NNInputStockData.load(pathlib.Path('NNInputStockData.pkl'))
        ref2 = obj.prepare_input(df)
        assert(np.allclose(ref1, ref2))
    
    def test_load_only(self):
        ''' Testing if we can load the NNInputStockData object and re-use it again '''
        df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
        ref1 = [-1.70059020e-02, 2.30333850e+04, -1.05423469e-01, 3.66213423e-02, -1.10082558e-01]
        # load
        obj = NNInputStockData.load(pathlib.Path('test.pkl'))
        ref2 = obj.prepare_input(df)
        assert(np.allclose(ref1, ref2))

class Test_live_df:
    def test_with_live_data(self):
        # Testing the NNInputStockData with live data, simulating how it will actually work 
        NNData = NNInputStockData()
        NNData.register_indicators([EMA50, BB24])

        df = read_csv(csv = pathlib.Path(__file__).parent / 'BTCUSDT_1d.csv')
        StockData = StockDataDF(df, normalize=False)

        for live_df in StockData.df_generator():
            if live_df.shape[0] <= NNData.required_period:
                continue
            obs = NNData.prepare_input(live_df)
            break
        ref = np.array([0.24029928, 0.42507829, 0.6098573, 0.10261542, 0.77361277, -0.06021854, -0.09433811, -0.15163344])
        assert(np.allclose(obs, ref))