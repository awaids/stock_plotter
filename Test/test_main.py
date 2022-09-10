from Helper import DataReader
import os
TEST_CSV = os.path.join(os.path.dirname(__file__), 'BTCUSDT_1d.csv')


class TestStockDataDF:
    df = DataReader.read_csv(csv=TEST_CSV)
    sliced_df = df.head().copy()
    sdata = DataReader.StockDataDF(sliced_df)

    def test_normalization(self):
        for col in ['High', 'Low', 'Close', 'Open']:
            assert(self.sdata.df[col].max() <= 1.0)

    def test_de_normalization(self):
        assert(self.sdata.de_normalize(1.0) == 4426.62), "De-normalized value of the max should be 4426.62"

