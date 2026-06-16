from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:
    import pyarrow.parquet as pq
except Exception:  # pragma: no cover
    pq = None


def read_parquet_compat(path: str | Path, columns: list[str] | None = None) -> pd.DataFrame:
    path = Path(path)
    try:
        return pd.read_parquet(path, columns=columns)
    except Exception:
        if pq is None:
            raise
        table = pq.read_table(path, columns=columns, use_pandas_metadata=False)
        return table.to_pandas(ignore_metadata=True)


def to_epoch_seconds(values: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(values):
        return values.astype("datetime64[ns]").astype("int64") // 10**9

    numeric = pd.to_numeric(values, errors="coerce")
    if numeric.notna().all():
        max_abs = float(numeric.abs().max()) if len(numeric) else 0
        if max_abs > 1e17:
            return (numeric // 10**9).astype("int64")
        if max_abs > 1e14:
            return (numeric // 10**6).astype("int64")
        if max_abs > 1e11:
            return (numeric // 10**3).astype("int64")
        return numeric.astype("int64")

    return pd.to_datetime(values).astype("datetime64[ns]").astype("int64") // 10**9


def normalize_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    required = {"time", "open", "high", "low", "close"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"OHLC dataframe missing columns: {sorted(missing)}")
    out = df.copy()
    out["time"] = pd.to_datetime(out["time"])
    out = out.drop_duplicates("time", keep="last").sort_values("time").reset_index(drop=True)
    return out


def normalize_for_visual_epoch(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "time" in out.columns:
        out["time_epoch"] = to_epoch_seconds(out["time"])
    return out


def format_mql_time(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    ts = pd.Timestamp(value)
    return ts.strftime("%Y.%m.%d %H:%M")
