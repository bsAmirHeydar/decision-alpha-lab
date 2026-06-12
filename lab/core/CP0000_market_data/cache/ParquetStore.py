import os
import pandas as pd


class ParquetStore:

    def __init__(self, base_path="lab/cache_data"):
        self.base_path = base_path

    def _file(self, symbol, timeframe):
        path = os.path.join(self.base_path, symbol, timeframe)
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, "data.parquet")

    def save(self, df, symbol, timeframe):
        df.to_parquet(self._file(symbol, timeframe), index=False)

    def load(self, symbol, timeframe):
        file = self._file(symbol, timeframe)

        if not os.path.exists(file):
            return None

        return pd.read_parquet(file)

    def delete(self, symbol, timeframe):
        file = self._file(symbol, timeframe)

        if os.path.exists(file):
            os.remove(file)