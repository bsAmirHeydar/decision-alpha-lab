#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, save_json


def load_decision_memories(common: Path, asset: str, timeframe: str):
    root = common / "astro_ml" / "antifragile_fragility_audits" / asset.upper() / timeframe.upper()
    memories = []
    if not root.exists():
        return memories
    for p in sorted(root.glob("*/antifragile_decision_memory.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            item = json.loads(p.read_text(encoding="utf-8"))
            item["_path"] = str(p)
            memories.append(item)
        except Exception:
            pass
    return memories


def main() -> int:
    ap = argparse.ArgumentParser(description="Export reusable Astro ML memory into a portable knowledge pack.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--out-json", default="")
    ap.add_argument("--out-md", default="")
    args = ap.parse_args()

    common = Path(args.common_files)
    mem = common / "astro_ml" / "memory" / args.asset / args.timeframe
    if not mem.exists():
        raise FileNotFoundError(mem)

    index_path = mem / "memory_index.csv"
    knowledge_path = mem / "knowledge_memory.jsonl"
    index = pd.read_csv(index_path) if index_path.exists() else pd.DataFrame()
    lessons = []
    if knowledge_path.exists():
        for line in knowledge_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    lessons.append(json.loads(line))
                except Exception:
                    pass

    model_cards = []
    runs = mem / "runs"
    if runs.exists():
        for p in runs.glob("*/model_card.json"):
            try:
                model_cards.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                pass

    decision_memories = load_decision_memories(common, args.asset, args.timeframe)
    hardened_principles = []
    for item in decision_memories:
        for hp in item.get("hardened_principles", []) or []:
            hardened_principles.append({
                "run_id": item.get("run_id", ""),
                "production_gate": item.get("production_gate", ""),
                **hp,
            })
    production_ready = [m for m in decision_memories if str(m.get("production_gate", "")) == "pass"]

    pack = {
        "asset": args.asset,
        "timeframe": args.timeframe,
        "memory_dir": str(mem),
        "run_count": int(len(index)) if not index.empty else 0,
        "lesson_count": len(lessons),
        "model_card_count": len(model_cards),
        "decision_memory_count": len(decision_memories),
        "production_ready_count": len(production_ready),
        "hardened_principle_count": len(hardened_principles),
        "memory_index": index.to_dict(orient="records") if not index.empty else [],
        "lessons": lessons,
        "model_cards": model_cards,
        "decision_memories": decision_memories,
        "production_ready_decision_memories": production_ready,
        "hardened_principles": hardened_principles,
    }

    out_json = Path(args.out_json) if args.out_json else mem / f"astro_knowledge_pack_{args.asset}_{args.timeframe}.json"
    out_md = Path(args.out_md) if args.out_md else mem / f"astro_knowledge_pack_{args.asset}_{args.timeframe}.md"
    ensure_dir(out_json.parent)
    save_json(out_json, pack)

    lines = [f"# Astro Knowledge Pack - {args.asset} {args.timeframe}\n"]
    lines.append(f"Runs: `{pack['run_count']}`")
    lines.append(f"Lessons: `{pack['lesson_count']}`")
    lines.append(f"Model cards: `{pack['model_card_count']}`\n")
    lines.append(f"Decision memories: `{pack['decision_memory_count']}`")
    lines.append(f"Production-ready memories: `{pack['production_ready_count']}`")
    lines.append(f"Hardened principles: `{pack['hardened_principle_count']}`\n")
    if not index.empty:
        lines.append("## Best runs by balanced accuracy\n")
        tmp = index.copy()
        if "balanced_accuracy" in tmp.columns:
            tmp["balanced_accuracy"] = pd.to_numeric(tmp["balanced_accuracy"], errors="coerce")
            tmp = tmp.sort_values("balanced_accuracy", ascending=False)
        for _, row in tmp.head(20).iterrows():
            lines.append(f"- `{row.get('run_id','')}` target=`{row.get('target','')}` balanced_accuracy=`{row.get('balanced_accuracy','')}` run_dir=`{row.get('run_dir','')}`")
    if production_ready:
        lines.append("\n## Production-ready decision memories\n")
        for item in production_ready[:20]:
            lines.append(f"- `{item.get('run_id','')}` hardened_principles=`{item.get('hardened_principles_count','')}` fragility_flags=`{item.get('fragility_flags_count','')}` gate=`{item.get('production_gate','')}`")
    if hardened_principles:
        lines.append("\n## Sample hardened principles\n")
        for item in hardened_principles[:30]:
            lines.append(f"- run=`{item.get('run_id','')}` principle=`{item.get('principle','')}` target=`{item.get('target','')}`")
    if lessons:
        lines.append("\n## Sample learned lessons\n")
        for item in lessons[-50:]:
            lesson = item.get("lesson", item)
            lines.append(f"- run=`{item.get('run_id','')}` {lesson}")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"ASTRO_KNOWLEDGE_PACK_JSON={out_json}")
    print(f"ASTRO_KNOWLEDGE_PACK_MD={out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
