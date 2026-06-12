import pandas as pd
from datetime import datetime, timedelta

from lab.core.CP0000_market_data.cache.ParquetStore import ParquetStore


class MarketDataEngine:

    def __init__(self, connector):
        self.connector = connector
        self.store = ParquetStore()

    def fetch(
        self,
        symbol,
        timeframe,
        bars=None,
        days=None,
        start=None,
        end=None,
        reset_cache: bool = False,
    ):

        cache_key = timeframe.name

        # -------------------------
        # RESET MODE
        # -------------------------
        if reset_cache:
            self.store.delete(symbol, cache_key)

        cached = self.store.load(symbol, cache_key)

        # -------------------------
        # CASE 1: NO CACHE
        # -------------------------
        if cached is None:
            df = self.connector.fetch(
                symbol=symbol,
                timeframe=timeframe,
                bars=bars,
                days=days,
                start=start,
                end=end,
            )

            self.store.save(df, symbol, cache_key)
            return df

        # -------------------------
        # CASE 2: CACHE EXISTS
        # -------------------------
        cached = cached.sort_values("time")

        last_time = cached["time"].max()

        # safe alignment (avoid MT5 overlap issues)
        start_time = last_time + timedelta(seconds=1)

        df_new = None

        try:
            df_new = self.connector.fetch(
                symbol=symbol,
                timeframe=timeframe,
                start=start_time,
                end=datetime.now(),
            )
        except Exception:
            return cached

        if df_new is None or df_new.empty:
            return cached

        # -------------------------
        # MERGE + CLEAN
        # -------------------------
        final = pd.concat([cached, df_new])

        final = final.drop_duplicates(subset=["time"])
        final = final.sort_values("time").reset_index(drop=True)

        self.store.save(final, symbol, cache_key)

        return final