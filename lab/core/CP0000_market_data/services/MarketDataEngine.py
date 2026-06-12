# lab/core/CP0000_market_data/services/MarketDataEngine.py

from datetime import datetime, timedelta
import pandas as pd

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

        if reset_cache:
            self.store.delete(symbol, cache_key)

        cached = self.store.load(symbol, cache_key)

        # ==========================================
        # CASE 1: Explicit range request
        # ==========================================
        if start is not None and end is not None:

            df_range = self.connector.fetch(
                symbol=symbol,
                timeframe=timeframe,
                start=start,
                end=end,
                strict=False,
            )

            if df_range is None or df_range.empty:
                return pd.DataFrame()

            if cached is None:
                final = (
                    df_range
                    .drop_duplicates(
                        subset=["time"],
                        keep="last",
                    )
                    .sort_values("time")
                    .reset_index(drop=True)
                )
            else:
                final = (
                    pd.concat([cached, df_range])
                    .drop_duplicates(
                        subset=["time"],
                        keep="last",
                    )
                    .sort_values("time")
                    .reset_index(drop=True)
                )

            self.store.save(
                final,
                symbol,
                cache_key,
            )

            return (
                final[
                    (final["time"] >= start)
                    & (final["time"] <= end)
                ]
                .reset_index(drop=True)
            )

        # ==========================================
        # CASE 2: No cache exists
        # ==========================================
        if cached is None:

            df = self.connector.fetch(
                symbol=symbol,
                timeframe=timeframe,
                bars=bars,
                days=days,
            )

            if df is None:
                return pd.DataFrame()

            df = (
                df
                .drop_duplicates(
                    subset=["time"],
                    keep="last",
                )
                .sort_values("time")
                .reset_index(drop=True)
            )

            self.store.save(
                df,
                symbol,
                cache_key,
            )

            return df

        # ==========================================
        # CASE 3: Cache exists → sync
        # ==========================================
        cached = (
            cached
            .drop_duplicates(
                subset=["time"],
                keep="last",
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

        last_time = cached["time"].max()

        # Re-fetch the last candle because it may
        # still be forming.
        start_sync = last_time

        try:
            df_new = self.connector.fetch(
                symbol=symbol,
                timeframe=timeframe,
                start=start_sync,
                end=datetime.now(),
                strict=False,
            )
        except Exception:
            df_new = pd.DataFrame()

        if df_new is not None and not df_new.empty:

            cached = (
                pd.concat([cached, df_new])
                .drop_duplicates(
                    subset=["time"],
                    keep="last",
                )
                .sort_values("time")
                .reset_index(drop=True)
            )

            self.store.save(
                cached,
                symbol,
                cache_key,
            )

        # ==========================================
        # Return modes
        # ==========================================

        # Latest N bars
        if bars is not None:
            return (
                cached
                .tail(bars)
                .reset_index(drop=True)
            )

        # Last N days
        if days is not None:

            cutoff = datetime.now() - timedelta(days=days)

            return (
                cached[
                    cached["time"] >= cutoff
                ]
                .reset_index(drop=True)
            )

        # Full archive
        return cached

    # ==================================================
    # Internal accessor
    # ==================================================

    def _get_df(self, symbol, timeframe):

        cache_key = timeframe.name

        df = self.store.load(
            symbol,
            cache_key,
        )

        if df is None:
            raise ValueError(
                "No cached data. Call fetch() first."
            )

        return (
            df
            .drop_duplicates(
                subset=["time"],
                keep="last",
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

    def _resolve_shift(self, df, shift: int):

        if shift < 0:
            raise ValueError(
                "Shift must be >= 0 (MQL5 style indexing)."
            )

        idx = len(df) - 1 - shift

        if idx < 0:
            raise IndexError(
                f"Shift {shift} is out of range."
            )

        return idx
    # ==================================================
    # Price accessors (MQL5 style)
    # ==================================================

    def iOpen(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["open"]


    def iClose(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["close"]


    def iHigh(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["high"]


    def iLow(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["low"]


    # ==================================================
    # Extra accessors (MQL5 style)
    # ==================================================

    def iTime(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["time"]


    def iVolume(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["tick_volume"]


    def iSpread(self, symbol, timeframe, shift: int):
        df = self._get_df(symbol, timeframe)

        idx = self._resolve_shift(df, shift)

        return df.iloc[idx]["spread"]