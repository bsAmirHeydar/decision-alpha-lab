import os
import pandas as pd


class ParquetStore:

    def __init__(self, base_path="lab/cache_data"):
        self.base_path = base_path

    def _file(self, symbol, timeframe):
        path = os.path.join(
            self.base_path,
            symbol,
            timeframe,
        )

        os.makedirs(path, exist_ok=True)

        filename = f"{symbol}_{timeframe}.parquet"

        return os.path.join(path, filename)

    def save(self, df, symbol, timeframe):

        if df is None or df.empty:
            return

        df = (
            df
            .drop_duplicates(subset=["time"])
            .sort_values("time")
            .reset_index(drop=True)
        )

        df.to_parquet(
            self._file(symbol, timeframe),
            index=False,
        )

    def load(self, symbol, timeframe):

        file = self._file(symbol, timeframe)

        if not os.path.exists(file):
            return None

        return pd.read_parquet(file)

    def delete(self, symbol, timeframe):

        file = self._file(symbol, timeframe)

        if os.path.exists(file):
            os.remove(file)

        folder = os.path.dirname(file)

        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)

            symbol_folder = os.path.dirname(folder)

            if (
                os.path.isdir(symbol_folder)
                and not os.listdir(symbol_folder)
            ):
                os.rmdir(symbol_folder)

    def exists(self, symbol, timeframe):

        return os.path.exists(
            self._file(symbol, timeframe)
        )