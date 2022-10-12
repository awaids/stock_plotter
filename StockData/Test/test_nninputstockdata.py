import pytest as py
import pandas as pd
from stock_plotter.StockData.NNInputStockData import IndicatorBase
from stock_plotter.StockData.NNInputStockData import NNInputStockData

class TestInd1(IndicatorBase):
    @staticmethod
    def get_period():
        return 1
    
    @staticmethod
    def add_indicator_col(df):
        pass

class TestInd2(IndicatorBase):
    @staticmethod
    def get_period():
        return 5

    @staticmethod
    def add_indicator_col(df):
        pass

def test_get_period():
    inputdata = NNInputStockData()
    inputdata.register_indicators(indicators=[TestInd1, TestInd2])
    assert(inputdata.period == 5), "Period must be the max period of all indicators"