#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, save_excel


def discover_decision_memories(common: Path, asset: str, timeframe: str) -> pd.DataFrame:
    root = common / "astro_ml" / "antifragile_fragility_audits" / asset.upper() / timeframe.upper()
    rows = []
    if not root.exists():
        return pd.DataFrame()
    for p in sorted(root.glob("*/antifragile_decision_memory.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            item = json.loads(p.read_text(encoding="utf-8"))
            rows.append({
                "run_id": item.get("run_id", p.parent.name),
                "created_utc": item.get("created_utc", ""),
                "production_gate": item.get("production_gate", ""),
                "hardened_principles_count": item.get("hardened_principles_count", 0),
                "fragility_flags_count": item.get("fragility_flags_count", 0),
                "targets": ",".join(item.get("targets", []) or []),
                "dataset_csv": item.get("dataset_csv", ""),
                "path": str(p),
            })
        except Exception:
            pass
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Query the persistent Astro ML memory store.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--memory-root", default="")
    ap.add_argument("--contains", default="", help="Optional text filter over learned lessons.")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--out-xlsx", default="")
    ap.add_argument("--production-only", action="store_true", help="Show only runs whose latest fragility memory passed the production gate.")
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
    decision_df = discover_decision_memories(common, args.asset, args.timeframe)
    if args.production_only and not decision_df.empty:
        production_targets = set()
        for raw in decision_df[decision_df["production_gate"].astype(str).eq("pass")]["targets"].astype(str):
            for t in [x.strip() for x in raw.split(",") if x.strip()]:
                production_targets.add(t)
        if not index.empty and "target" in index.columns:
            index = index[index["target"].astype(str).isin(production_targets)].copy()
        if not lessons_df.empty and "run_id" in lessons_df.columns:
            if "target" in lessons_df.columns:
                lessons_df = lessons_df[lessons_df["target"].astype(str).isin(production_targets)].copy()
        decision_df = decision_df[decision_df["production_gate"].astype(str).eq("pass")].copy()
    out_xlsx = Path(args.out_xlsx) if args.out_xlsx else mem / "memory_query.xlsx"
    save_excel(out_xlsx, {"Runs": index, "Lessons": lessons_df, "DecisionMemory": decision_df})
    print(f"ASTRO_ML_MEMORY_DIR={mem}")
    print(f"ASTRO_ML_MEMORY_QUERY_XLSX={out_xlsx}")
    if not index.empty:
        print(index.tail(10).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
