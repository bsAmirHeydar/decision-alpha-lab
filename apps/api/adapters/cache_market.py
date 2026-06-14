from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class CacheMarketDataEngine:
    """Minimal engine adapter for the UI API.

    It intentionally exposes the same `get_df(symbol, timeframe)` method used
    by LRuleNodeDetector and M0001RTV, while reading only reproducible parquet
    cache files.
    """

    base_path: Path

    def _file(self, symbol: str, timeframe) -> Path:
        timeframe_name = getattr(timeframe, "name", str(timeframe))
        return self.base_path / symbol / timeframe_name / f"{symbol}_{timeframe_name}.parquet"

    def exists(self, symbol: str, timeframe) -> bool:
        return self._file(symbol, timeframe).exists()

    def get_df(self, symbol: str, timeframe) -> pd.DataFrame:
        file = self._file(symbol, timeframe)
        if not file.exists():
            raise FileNotFoundError(f"No candle cache found: {file}")
        df = pd.read_parquet(file)
        if df.empty:
            return df
        return (
            df.drop_duplicates(subset=["time"], keep="last")
            .sort_values("time")
            .reset_index(drop=True)
        )
