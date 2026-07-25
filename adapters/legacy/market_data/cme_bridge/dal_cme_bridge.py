"""Local CME-compatible DAL data bridge.

This is a legal/entitlement-neutral bridge. It has two immediately usable modes:

1) replay_csv: serve historical candle CSVs over localhost for research tools.
2) live_csv_tail: continuously copy vendor/CME-updated CSVs into MT5 Common Files
   so the MQL5 IMD expert can read live candles without DLL/WebSocket parsing.

Direct CME WebSocket/DataMine adapters are intentionally left behind this stable
bridge boundary because they require credentials, entitlements, product IDs, and
vendor-specific schemas. Add the official/vendor adapter in this process, not in
MQL5.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class BridgeConfig:
    host: str
    port: int
    source_dir: Path
    mt5_common_dir: Path
    symbols: dict[str, str]
    poll_seconds: float


def load_config(path: Path) -> BridgeConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return BridgeConfig(
        host=raw.get("host", "127.0.0.1"),
        port=int(raw.get("port", 8765)),
        source_dir=Path(raw.get("source_dir", "data/cme/bars")).expanduser(),
        mt5_common_dir=Path(raw.get("mt5_common_dir", "")).expanduser(),
        symbols=dict(raw.get("symbols", {})),
        poll_seconds=float(raw.get("poll_seconds", 1.0)),
    )


def read_bars_csv(path: Path, limit: int = 500) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    if limit > 0:
        rows = rows[-limit:]
    return rows


def ensure_mt5_schema(src: Path, dst: Path) -> None:
    """Copy a candle CSV into the strict MQL5-readable schema.

    Output header: time,open,high,low,close,volume
    Accepted source time columns: time, time_utc, datetime.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        return
    with src.open("r", encoding="utf-8", newline="") as f_in, dst.open("w", encoding="utf-8", newline="") as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        writer.writerow(["time", "open", "high", "low", "close", "volume"])
        for row in reader:
            ts = row.get("time") or row.get("time_utc") or row.get("datetime")
            if not ts:
                continue
            writer.writerow([
                ts,
                row.get("open", ""),
                row.get("high", ""),
                row.get("low", ""),
                row.get("close", ""),
                row.get("volume", row.get("tick_volume", "0")),
            ])


class BridgeServer:
    def __init__(self, config: BridgeConfig) -> None:
        self.config = config

    def make_handler(self):
        config = self.config

        class Handler(BaseHTTPRequestHandler):
            def _json(self, payload: object, status: int = 200) -> None:
                body = json.dumps(payload, default=str).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:  # noqa: N802
                url = urlparse(self.path)
                q = parse_qs(url.query)
                if url.path == "/health":
                    self._json({"ok": True, "time_utc": datetime.now(timezone.utc).isoformat(), "symbols": list(config.symbols)})
                    return
                if url.path == "/bars":
                    symbol = q.get("symbol", [""])[0]
                    limit = int(q.get("limit", ["500"])[0])
                    file_name = config.symbols.get(symbol, f"{symbol}_M1.csv")
                    rows = read_bars_csv(config.source_dir / file_name, limit)
                    self._json({"symbol": symbol, "count": len(rows), "bars": rows})
                    return
                self._json({"error": "not found"}, 404)

            def log_message(self, fmt: str, *args: object) -> None:
                print("bridge", fmt % args)

        return Handler

    def serve(self) -> None:
        server = ThreadingHTTPServer((self.config.host, self.config.port), self.make_handler())
        print(f"DAL bridge listening on http://{self.config.host}:{self.config.port}")
        server.serve_forever()


def live_csv_tail(config: BridgeConfig) -> None:
    if not config.mt5_common_dir:
        raise SystemExit("mt5_common_dir is required for live_csv_tail mode")
    print("DAL live CSV tail started")
    print("source_dir=", config.source_dir)
    print("mt5_common_dir=", config.mt5_common_dir)
    while True:
        for symbol, file_name in config.symbols.items():
            src = config.source_dir / file_name
            dst = config.mt5_common_dir / "Files" / "dal" / "cme" / f"{symbol}_M1.csv"
            if src.exists():
                try:
                    ensure_mt5_schema(src, dst)
                    print(f"updated {symbol}: {dst}")
                except Exception as exc:  # noqa: BLE001
                    print(f"copy failed symbol={symbol} err={exc}")
        time.sleep(config.poll_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decision Alpha Lab CME-compatible local data bridge")
    parser.add_argument("--config", default="adapters/legacy/market_data/cme_bridge/dal_cme_config.example.json")
    parser.add_argument("--mode", choices=["serve", "live_csv_tail"], default="serve")
    args = parser.parse_args()
    config = load_config(Path(args.config))
    if args.mode == "serve":
        BridgeServer(config).serve()
    else:
        live_csv_tail(config)


if __name__ == "__main__":
    main()
