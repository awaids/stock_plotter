import pytest
from Helper import Functions
from Helper import DataReader
import pandas as pd
import os

TEST_CSV = os.path.join(os.path.dirname(__file__), 'BTCUSDT_1d.csv')

def test_read_csv():
    df = DataReader.read_csv(csv=TEST_CSV, normalize=True)
    assert(df['High'].max() == 1.0)