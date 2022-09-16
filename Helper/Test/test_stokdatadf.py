import pytest
import numpy as np
from stock_plotter.Helper import DataReader 

import os
TEST_CSV = os.path.join(os.path.dirname(__file__), 'test_data.csv')


class TestStockDataDF:
    df = DataReader.read_csv(csv=TEST_CSV)
    sdata = DataReader.StockDataDF(df)

    def test_df(self):
        # Test if colums are correct
        assert({'High', 'Low', 'Close', 'Open',} == set(self.df.columns)), "Columns dont match"

    def test_num_entries(self):
        # Test the num_entroes function
        assert(self.sdata.num_entries == 2), "Num entries should 2"

    def test_normalization(self):
        # Test if the normalization works
        for col in ['High', 'Low', 'Close', 'Open']:
            assert(self.sdata.df[col].max() <= 1.0)

    def test_de_normalization(self):
        assert(self.sdata.de_normalize(1.0) == 225.0), "De-normalized value of the max should be 225.0"

    def test_live_generator(self):
        df_gen =  self.sdata.df_generator()
        # Set the denormalize function
        de_normalize = lambda e: self.sdata.de_normalize(e)

        # Here the df should have only one row
        ref = np.array([[100.,200.,50.,150.]])
        element = de_normalize(next(df_gen).to_numpy())
        # print(f'ref: {ref}\nval: {element}')
        assert(len(element) == 1), "First iteration should return a single row"
        assert((ref == element).all()), "Ref doen not match the actual value"

        # Here the df should have 2 rows
        element = de_normalize(next(df_gen).to_numpy())
        ref = np.array([[100.,200.,50.,150.],[150.,225.,110.,120.]])
        # print(f'ref: {ref}\nval: {element}')
        assert(len(element) == 2), "Second iteration should return two rows"
        assert((ref == element).all()), "Ref doen not match the actual value"
        
        # As the df is only 2 rows next should throw
        with pytest.raises(StopIteration):
            next(df_gen)
    
    def test_get_last_close(self):
        df_gen =  self.sdata.df_generator()
        assert(self.sdata.get_last_close(next(df_gen)) == 150)
        assert(self.sdata.get_last_close(next(df_gen)) == 120)
