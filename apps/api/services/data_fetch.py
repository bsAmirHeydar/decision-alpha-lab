from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:
    import pyarrow.parquet as pq
except Exception:  # pragma: no cover - optional fallback
    pq = None

from apps.api.core.config import settings


def root() -> Path:
    return settings.root_path.resolve()


def cache_file(symbol: str, timeframe: str) -> Path:
    return root() / "lab/cache_data" / symbol / timeframe / f"{symbol}_{timeframe}.parquet"


def fallback_cache_file(symbol: str, timeframe: str) -> Path:
    return root() / "lab/cache_data" / symbol / timeframe / "data.parquet"



def read_parquet_compat(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    try:
        return pd.read_parquet(path, columns=columns)
    except Exception:
        if pq is None:
            raise
        table = pq.read_table(path, columns=columns, use_pandas_metadata=False)
        return table.to_pandas(ignore_metadata=True)


def cache_candidates(symbol: str, timeframe: str) -> list[Path]:
    folder = root() / "lab/cache_data" / symbol / timeframe
    candidates = [
        folder / f"{symbol}_{timeframe}.parquet",
        folder / "data.parquet",
    ]
    if folder.exists():
        for extra in sorted(folder.glob("*.parquet")):
            if extra not in candidates:
                candidates.append(extra)
    return candidates


def choose_best_cache_file(symbol: str, timeframe: str) -> tuple[Path, pd.DataFrame] | None:
    best: tuple[Path, pd.DataFrame] | None = None
    required = {"time", "open", "high", "low", "close"}
    for file in cache_candidates(symbol, timeframe):
        if not file.exists():
            continue
        try:
            df = read_parquet_compat(file, columns=["time", "open", "high", "low", "close"])
            if not required.issubset(df.columns):
                continue
            if best is None or len(df) > len(best[1]):
                best = (file, df)
        except Exception:
            continue
    return best


def list_cached_datasets() -> list[dict[str, Any]]:
    base = root() / "lab/cache_data"
    if not base.exists():
        return []

    rows: list[dict[str, Any]] = []
    for symbol_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        for tf_dir in sorted(p for p in symbol_dir.iterdir() if p.is_dir()):
            best = choose_best_cache_file(symbol_dir.name, tf_dir.name)
            if best is None:
                continue
            existing, df = best
            rows_count = int(len(df))
            start = iso_time(df["time"].min()) if rows_count else None
            end = iso_time(df["time"].max()) if rows_count else None
            rows.append({
                "symbol": symbol_dir.name,
                "timeframe": tf_dir.name,
                "source": "cache",
                "path": existing.relative_to(root()).as_posix(),
                "rows": rows_count,
                "start": start,
                "end": end,
            })
    return rows


def fetch_market_data(
    symbol: str,
    timeframe: str,
    bars: int = 5000,
    source: str = "cache",
    reset_cache: bool = False,
) -> dict[str, Any]:
    symbol = symbol.strip()
    timeframe = timeframe.strip().upper()
    if not symbol:
        raise ValueError("Symbol is required")
    if not timeframe:
        raise ValueError("Timeframe is required")

    if source == "cache":
        return inspect_cache(symbol, timeframe)

    if source != "mt5":
        raise ValueError(f"Unsupported data source: {source}")

    return fetch_from_mt5(symbol=symbol, timeframe=timeframe, bars=bars, reset_cache=reset_cache)


def inspect_cache(symbol: str, timeframe: str) -> dict[str, Any]:
    best = choose_best_cache_file(symbol, timeframe)
    if best is None:
        raise FileNotFoundError(f"No readable cached data found for {symbol} {timeframe}")

    file, df = best
    return {
        "status": "ok",
        "source": "cache",
        "symbol": symbol,
        "timeframe": timeframe,
        "rows": int(len(df)),
        "start": iso_time(df["time"].min()) if len(df) and "time" in df.columns else None,
        "end": iso_time(df["time"].max()) if len(df) and "time" in df.columns else None,
        "path": file.relative_to(root()).as_posix(),
        "message": "Cached market data is available.",
    }


def fetch_from_mt5(symbol: str, timeframe: str, bars: int, reset_cache: bool) -> dict[str, Any]:
    try:
        from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
        from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
        from lab.core.CP0000_market_data.utils.timeframes import Timeframe
    except Exception as exc:
        raise RuntimeError(f"MT5 stack is not available in this Python environment: {exc}") from exc

    if not hasattr(Timeframe, timeframe):
        raise ValueError(f"Unknown timeframe: {timeframe}")

    tf = getattr(Timeframe, timeframe)
    connector = MT5Connector()
    connector.connect()
    try:
        engine = MarketDataEngine(connector)
        df = engine.fetch(symbol=symbol, timeframe=tf, bars=bars, reset_cache=reset_cache)
    finally:
        try:
            connector.disconnect()
        except Exception:
            pass

    if df is None or df.empty:
        raise RuntimeError(f"MT5 returned no data for {symbol} {timeframe}")

    file = cache_file(symbol, timeframe)
    return {
        "status": "ok",
        "source": "mt5",
        "symbol": symbol,
        "timeframe": timeframe,
        "rows": int(len(df)),
        "start": iso_time(df["time"].min()) if "time" in df.columns else None,
        "end": iso_time(df["time"].max()) if "time" in df.columns else None,
        "path": file.relative_to(root()).as_posix() if file.exists() else None,
        "message": "MT5 data fetched and cache was updated.",
    }


def iso_time(value: Any) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    try:
        return pd.to_datetime(value).isoformat()
    except Exception:
        return str(value)
