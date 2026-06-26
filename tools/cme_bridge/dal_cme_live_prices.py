"""One-command entrypoint for CME-price bridge providers.

Providers:
  databento_historical  Real CME/Globex historical bars through Databento.
  databento_live        Real CME/Globex live bars through Databento.
  yahoo_delayed         Delayed ES/NQ futures fallback through Yahoo Finance.

The output is always canonical DAL CSV:
    data/cme/bars/ES_M1.csv
    data/cme/bars/NQ_M1.csv
which can then be copied into MT5 Common Files with dal_cme_bridge.py
live_csv_tail, or read directly by the Python experiment runner.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str]) -> int:
    print("RUN", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="DAL CME live prices bridge launcher")
    parser.add_argument("provider", choices=["databento_historical", "databento_live", "yahoo_delayed"])
    parser.add_argument("--config")
    parser.add_argument("--start")
    parser.add_argument("--end")
    args = parser.parse_args()

    py = sys.executable
    if args.provider == "databento_historical":
        config = args.config or "tools/cme_bridge/configs/databento_es_nq.example.json"
        if not args.start or not args.end:
            raise SystemExit("databento_historical requires --start and --end")
        raise SystemExit(run([py, "tools/cme_bridge/providers/databento_provider.py", "--mode", "historical", "--config", config, "--start", args.start, "--end", args.end]))
    if args.provider == "databento_live":
        config = args.config or "tools/cme_bridge/configs/databento_es_nq.example.json"
        cmd = [py, "tools/cme_bridge/providers/databento_provider.py", "--mode", "live", "--config", config]
        if args.start:
            cmd += ["--start", args.start]
        raise SystemExit(run(cmd))
    if args.provider == "yahoo_delayed":
        config = args.config or "tools/cme_bridge/configs/yahoo_delayed_es_nq.example.json"
        raise SystemExit(run([py, "tools/cme_bridge/providers/yahoo_delayed_provider.py", "--mode", "poll", "--config", config]))


if __name__ == "__main__":
    main()
