#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, save_excel


def main() -> int:
    ap = argparse.ArgumentParser(description="Query the persistent Astro ML memory store.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--memory-root", default="")
    ap.add_argument("--contains", default="", help="Optional text filter over learned lessons.")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--out-xlsx", default="")
    args = ap.parse_args()

    common = Path(args.common_files)
    root = Path(args.memory_root) if args.memory_root else common / "astro_ml" / "memory"
    mem = root / args.asset / args.timeframe
    index_path = mem / "memory_index.csv"
    knowledge_path = mem / "knowledge_memory.jsonl"
    index = pd.read_csv(index_path) if index_path.exists() else pd.DataFrame()
    lessons = []
    if knowledge_path.exists():
        with knowledge_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                if args.contains and args.contains.lower() not in json.dumps(item, ensure_ascii=False).lower():
                    continue
                lessons.append(item)
    lessons_df = pd.DataFrame(lessons)
    out_xlsx = Path(args.out_xlsx) if args.out_xlsx else mem / "memory_query.xlsx"
    save_excel(out_xlsx, {"Runs": index, "Lessons": lessons_df})
    print(f"ASTRO_ML_MEMORY_DIR={mem}")
    print(f"ASTRO_ML_MEMORY_QUERY_XLSX={out_xlsx}")
    if not index.empty:
        print(index.tail(10).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
