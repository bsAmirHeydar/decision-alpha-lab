"""CSV bar store shared by DAL CME bridge providers.

Writes canonical MQL5-readable candle CSV files:
    time,open,high,low,close,volume

This module only stores legally obtained data. It does not provide market-data
entitlements and does not bypass any exchange/vendor license.
"""
from __future__ import annotations

import csv
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


HEADER = ["time", "open", "high", "low", "close", "volume"]


@dataclass(frozen=True)
class CsvBar:
    symbol: str
    time_utc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def normalized_time(self) -> str:
        dt = self.time_utc
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def as_row(self) -> list[str]:
        return [
            self.normalized_time(),
            _fmt(self.open),
            _fmt(self.high),
            _fmt(self.low),
            _fmt(self.close),
            str(int(self.volume)) if float(self.volume).is_integer() else _fmt(self.volume),
        ]


def _fmt(value: float) -> str:
    return (f"{float(value):.10f}").rstrip("0").rstrip(".")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_existing(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if row.get("time"):
                rows.append({k: row.get(k, "") for k in HEADER})
        return rows


def atomic_write_rows(path: Path, rows: Iterable[dict[str, str] | list[str]]) -> None:
    ensure_parent(path)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    Path(tmp_name).unlink(missing_ok=True)
    tmp_path = Path(tmp_name)
    try:
        with tmp_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow([row.get(k, "") for k in HEADER])
                else:
                    writer.writerow(row)
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)


def append_or_replace_bar(path: Path, bar: CsvBar, max_rows: int = 5000) -> None:
    rows = read_existing(path)
    new_row = dict(zip(HEADER, bar.as_row()))
    if rows and rows[-1].get("time") == new_row["time"]:
        rows[-1] = new_row
    else:
        rows.append(new_row)
    if max_rows > 0 and len(rows) > max_rows:
        rows = rows[-max_rows:]
    atomic_write_rows(path, rows)


def write_bars(path: Path, bars: Iterable[CsvBar], max_rows: int = 0) -> int:
    rows = [dict(zip(HEADER, b.as_row())) for b in bars]
    if max_rows > 0 and len(rows) > max_rows:
        rows = rows[-max_rows:]
    atomic_write_rows(path, rows)
    return len(rows)
