"""Yahoo delayed CME futures fallback provider.

This is NOT a direct CME real-time feed and is NOT suitable for live trading.
It is useful when you only need a quick delayed ES/NQ sanity feed and do not yet
have Databento/CME credentials. Yahoo pages label ES=F and NQ=F as CME delayed
quotes; availability and delay can change.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd  # type: ignore
except Exception:  # noqa: BLE001
    pd = None

from tools.cme_bridge.dal_bar_store import CsvBar, write_bars


@dataclass(frozen=True)
class YahooConfig:
    output_dir: Path
    symbols: dict[str, str]
    interval: str = "1m"
    period: str = "1d"
    poll_seconds: float = 15.0
    max_rows: int = 2000


def load_config(path: Path) -> YahooConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return YahooConfig(
        output_dir=Path(raw.get("output_dir", "data/cme/bars")).expanduser(),
        symbols=dict(raw.get("symbols", {"ES": "ES=F", "NQ": "NQ=F"})),
        interval=raw.get("interval", "1m"),
        period=raw.get("period", "1d"),
        poll_seconds=float(raw.get("poll_seconds", 15.0)),
        max_rows=int(raw.get("max_rows", 2000)),
    )


def require_yfinance():
    try:
        import yfinance as yf  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise SystemExit("yfinance is not installed. Run: pip install -U yfinance pandas") from exc
    return yf


def to_dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif pd is not None:
        dt = pd.Timestamp(value).to_pydatetime()
    else:
        dt = datetime.fromisoformat(str(value))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def frame_to_bars(alias: str, frame: Any) -> list[CsvBar]:
    bars: list[CsvBar] = []
    if frame is None or len(frame) == 0:
        return bars
    df = frame.reset_index()
    time_col = "Datetime" if "Datetime" in df.columns else ("Date" if "Date" in df.columns else df.columns[0])
    for _, row in df.iterrows():
        try:
            bars.append(
                CsvBar(
                    symbol=alias,
                    time_utc=to_dt(row[time_col]),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=float(row.get("Volume", 0) or 0),
                )
            )
        except Exception:  # noqa: BLE001
            continue
    return bars


def fetch_once(config: YahooConfig) -> None:
    yf = require_yfinance()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    for alias, ticker in config.symbols.items():
        frame = yf.download(ticker, period=config.period, interval=config.interval, progress=False, auto_adjust=False)
        bars = frame_to_bars(alias, frame)
        out = config.output_dir / f"{alias}_M1.csv"
        n = write_bars(out, bars[-config.max_rows :], max_rows=config.max_rows)
        last = bars[-1].normalized_time() if bars else "none"
        print(f"{alias} <- {ticker}: wrote {n} delayed bars last={last} -> {out}")


def live_poll(config: YahooConfig) -> None:
    print("Yahoo delayed polling started. This is not direct real-time CME data.")
    while True:
        try:
            fetch_once(config)
        except Exception as exc:  # noqa: BLE001
            print(f"yahoo delayed poll failed: {exc}")
        time.sleep(config.poll_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="DAL Yahoo delayed CME futures fallback bridge")
    parser.add_argument("--config", default="tools/cme_bridge/configs/yahoo_delayed_es_nq.example.json")
    parser.add_argument("--mode", choices=["once", "poll"], default="poll")
    args = parser.parse_args()
    config = load_config(Path(args.config))
    if args.mode == "once":
        fetch_once(config)
    else:
        live_poll(config)


if __name__ == "__main__":
    main()
