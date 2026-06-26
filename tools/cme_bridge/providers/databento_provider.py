"""Databento provider for CME/Globex ES/NQ live and historical bars.

Databento is an official licensed market data provider with CME Globex MDP3 data.
This adapter expects you to have a Databento account, CME entitlements, and a
DATABENTO_API_KEY environment variable.

Recommended symbols:
    ES.c.0, NQ.c.0 with stype_in=continuous
or:
    ES.FUT, NQ.FUT with stype_in=parent

The adapter writes canonical DAL CSV bars for MQL5:
    time,open,high,low,close,volume
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd  # type: ignore
except Exception:  # noqa: BLE001
    pd = None

from tools.cme_bridge.dal_bar_store import CsvBar, append_or_replace_bar, write_bars


@dataclass(frozen=True)
class DatabentoSymbol:
    alias: str
    databento_symbol: str


@dataclass(frozen=True)
class DatabentoConfig:
    dataset: str
    schema: str
    stype_in: str
    output_dir: Path
    symbols: list[DatabentoSymbol]
    max_rows: int = 5000
    poll_status_seconds: float = 10.0


def load_config(path: Path) -> DatabentoConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    symbols = [DatabentoSymbol(alias=k, databento_symbol=v) for k, v in dict(raw.get("symbols", {})).items()]
    if not symbols:
        raise SystemExit("config.symbols is empty")
    return DatabentoConfig(
        dataset=raw.get("dataset", "GLBX.MDP3"),
        schema=raw.get("schema", "ohlcv-1m"),
        stype_in=raw.get("stype_in", "continuous"),
        output_dir=Path(raw.get("output_dir", "data/cme/bars")).expanduser(),
        symbols=symbols,
        max_rows=int(raw.get("max_rows", 5000)),
        poll_status_seconds=float(raw.get("poll_status_seconds", 10.0)),
    )


def require_databento():
    try:
        import databento as db  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(
            "databento package is not installed. Run: pip install -U databento pandas\n"
            "Also set DATABENTO_API_KEY in your environment."
        ) from exc
    return db


def to_utc_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        # Databento timestamps are commonly nanoseconds since epoch.
        v = int(value)
        if v > 10_000_000_000_000_000:
            dt = datetime.fromtimestamp(v / 1_000_000_000, tz=timezone.utc)
        elif v > 10_000_000_000:
            dt = datetime.fromtimestamp(v / 1000, tz=timezone.utc)
        else:
            dt = datetime.fromtimestamp(v, tz=timezone.utc)
    else:
        # pandas handles ISO strings and Timestamp objects.
        if pd is None:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        else:
            dt = pd.Timestamp(value).to_pydatetime()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def price_value(x: Any) -> float:
    if x is None:
        raise ValueError("missing price")
    # Databento DBN Python usually exposes scaled prices as decimal-like values.
    return float(x)


def record_to_bar(alias: str, record: Any) -> CsvBar | None:
    # OHLCV record attribute names in the official client are exposed as fields.
    # This function is intentionally defensive across databento versions.
    t = getattr(record, "ts_event", None) or getattr(record, "time", None) or getattr(record, "ts_recv", None)
    if t is None:
        return None
    fields = {"open": None, "high": None, "low": None, "close": None, "volume": 0}
    for k in list(fields):
        if hasattr(record, k):
            fields[k] = getattr(record, k)
    if fields["open"] is None or fields["high"] is None or fields["low"] is None or fields["close"] is None:
        return None
    return CsvBar(
        symbol=alias,
        time_utc=to_utc_datetime(t),
        open=price_value(fields["open"]),
        high=price_value(fields["high"]),
        low=price_value(fields["low"]),
        close=price_value(fields["close"]),
        volume=float(fields.get("volume") or 0),
    )


def dataframe_to_bars(alias: str, df: Any) -> list[CsvBar]:
    bars: list[CsvBar] = []
    if df is None or len(df) == 0:
        return bars
    frame = df.reset_index()
    # Accept common DBN/pandas column layouts.
    time_col = "ts_event" if "ts_event" in frame.columns else "index"
    for _, row in frame.iterrows():
        try:
            bars.append(
                CsvBar(
                    symbol=alias,
                    time_utc=to_utc_datetime(row[time_col]),
                    open=price_value(row["open"]),
                    high=price_value(row["high"]),
                    low=price_value(row["low"]),
                    close=price_value(row["close"]),
                    volume=float(row.get("volume", 0) or 0),
                )
            )
        except Exception as exc:  # noqa: BLE001
            print(f"skip bad row alias={alias}: {exc}")
    return bars


def historical(config: DatabentoConfig, start: str, end: str, key: str | None) -> None:
    db = require_databento()
    client = db.Historical(key=key) if key else db.Historical()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    for spec in config.symbols:
        print(f"request historical {spec.alias} <- {spec.databento_symbol} {start}..{end}")
        data = client.timeseries.get_range(
            dataset=config.dataset,
            schema=config.schema,
            symbols=spec.databento_symbol,
            stype_in=config.stype_in,
            start=start,
            end=end,
        )
        df = data.to_df()
        bars = dataframe_to_bars(spec.alias, df)
        out = config.output_dir / f"{spec.alias}_M1.csv"
        n = write_bars(out, bars, max_rows=0)
        print(f"wrote {n} bars -> {out}")


class LiveSymbolRunner:
    def __init__(self, config: DatabentoConfig, spec: DatabentoSymbol, key: str | None, replay_start: str | None) -> None:
        self.config = config
        self.spec = spec
        self.key = key
        self.replay_start = replay_start
        self.seen = 0
        self.last_bar_time: datetime | None = None
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        db = require_databento()
        client = db.Live(key=self.key) if self.key else db.Live()
        kwargs: dict[str, Any] = {}
        if self.replay_start:
            kwargs["start"] = self.replay_start
        print(f"live subscribe {self.spec.alias} <- {self.spec.databento_symbol} schema={self.config.schema}")
        client.subscribe(
            dataset=self.config.dataset,
            schema=self.config.schema,
            stype_in=self.config.stype_in,
            symbols=self.spec.databento_symbol,
            **kwargs,
        )

        def on_record(record: Any) -> None:
            bar = record_to_bar(self.spec.alias, record)
            if bar is None:
                return
            out = self.config.output_dir / f"{self.spec.alias}_M1.csv"
            append_or_replace_bar(out, bar, max_rows=self.config.max_rows)
            self.seen += 1
            self.last_bar_time = bar.time_utc
            print(f"{self.spec.alias} {bar.normalized_time()} O={bar.open} H={bar.high} L={bar.low} C={bar.close} V={bar.volume}")

        def on_error(exc: Exception) -> None:
            print(f"databento callback error alias={self.spec.alias}: {exc}", file=sys.stderr)

        client.add_callback(record_callback=on_record, exception_callback=on_error)
        client.start()
        try:
            while not self._stop.is_set():
                time.sleep(0.5)
        finally:
            try:
                client.stop()
            except Exception:  # noqa: BLE001
                try:
                    client.terminate()
                except Exception:
                    pass


def live(config: DatabentoConfig, key: str | None, replay_start: str | None) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    runners = [LiveSymbolRunner(config, spec, key, replay_start) for spec in config.symbols]
    threads = [threading.Thread(target=r.run, name=f"db-live-{r.spec.alias}", daemon=True) for r in runners]

    stopping = False

    def handle_signal(_sig: int, _frame: Any) -> None:
        nonlocal stopping
        stopping = True
        print("stopping databento live bridge...")
        for r in runners:
            r.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    for t in threads:
        t.start()
    while not stopping:
        time.sleep(config.poll_status_seconds)
        status = ", ".join(f"{r.spec.alias}:seen={r.seen}:last={r.last_bar_time}" for r in runners)
        print("live status", status)


def main() -> None:
    parser = argparse.ArgumentParser(description="DAL Databento CME live/historical bridge")
    parser.add_argument("--config", default="tools/cme_bridge/configs/databento_es_nq.example.json")
    parser.add_argument("--mode", choices=["historical", "live"], required=True)
    parser.add_argument("--start", help="Historical start ISO time/date, or live intraday replay start")
    parser.add_argument("--end", help="Historical end ISO time/date")
    parser.add_argument("--key", default=os.getenv("DATABENTO_API_KEY"), help="Databento API key; defaults to DATABENTO_API_KEY")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    if args.mode == "historical":
        if not args.start or not args.end:
            raise SystemExit("historical mode requires --start and --end")
        historical(config, start=args.start, end=args.end, key=args.key)
    else:
        live(config, key=args.key, replay_start=args.start)


if __name__ == "__main__":
    main()
