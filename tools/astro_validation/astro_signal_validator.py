#!/usr/bin/env python3
"""
Validate astro-only paper journals without touching market-side logic.

This tool does not judge profitability. It audits the signal surface itself:
- phase/action balance
- direction symmetry
- hold-duration profile
- threshold sensitivity
- shuffled baseline on the action stream
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Dict, List


def load_rows(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_float(row: dict, key: str) -> float:
    try:
        return float(row.get(key, "") or 0.0)
    except ValueError:
        return 0.0


def as_int(row: dict, key: str) -> int:
    try:
        return int(float(row.get(key, "") or 0))
    except ValueError:
        return 0


def summarize(rows: List[dict], *, entry_threshold: float, exit_threshold: float) -> Dict[str, object]:
    phase_counts = Counter(row.get("phase", "") for row in rows)
    action_counts = Counter(row.get("action", "") for row in rows)
    direction_counts = Counter(row.get("position_direction", "") for row in rows)
    regime_counts = Counter(row.get("regime_name", "") for row in rows)
    doctrine_counts = Counter(row.get("doctrine_id", "") for row in rows)
    schema_counts = Counter(row.get("schema_version", "") for row in rows)

    entry_scores = [as_float(r, "entry_score") for r in rows]
    exit_scores = [as_float(r, "exit_score") for r in rows]
    hold_bars = [as_int(r, "hold_bars") for r in rows if as_int(r, "hold_bars") > 0]

    armed_or_enter = sum(1 for r in rows if as_float(r, "entry_score") >= entry_threshold)
    reduce_or_exit = sum(1 for r in rows if as_float(r, "exit_score") >= exit_threshold)
    opposite_collisions = sum(1 for r in rows if "collision=opposite_entry" in (r.get("reason", "") or ""))

    doctrine_stability = len(doctrine_counts) == 1
    schema_stability = len(schema_counts) == 1

    return {
        "rows": len(rows),
        "phase_counts": dict(phase_counts),
        "action_counts": dict(action_counts),
        "direction_counts": dict(direction_counts),
        "regime_counts": dict(regime_counts),
        "doctrine_counts": dict(doctrine_counts),
        "schema_counts": dict(schema_counts),
        "doctrine_stability": doctrine_stability,
        "schema_stability": schema_stability,
        "avg_entry_score": mean(entry_scores) if entry_scores else 0.0,
        "avg_exit_score": mean(exit_scores) if exit_scores else 0.0,
        "avg_hold_bars": mean(hold_bars) if hold_bars else 0.0,
        "max_hold_bars": max(hold_bars) if hold_bars else 0,
        "entry_threshold_hits": armed_or_enter,
        "exit_threshold_hits": reduce_or_exit,
        "opposite_signal_collisions": opposite_collisions,
    }


def threshold_grid(rows: List[dict], entry_values: List[float], exit_values: List[float]) -> List[dict]:
    grid: List[dict] = []
    for entry_threshold in entry_values:
        for exit_threshold in exit_values:
            entry_hits = sum(1 for r in rows if as_float(r, "entry_score") >= entry_threshold)
            exit_hits = sum(1 for r in rows if as_float(r, "exit_score") >= exit_threshold)
            grid.append(
                {
                    "entry_threshold": entry_threshold,
                    "exit_threshold": exit_threshold,
                    "entry_hits": entry_hits,
                    "exit_hits": exit_hits,
                    "hit_balance": entry_hits - exit_hits,
                }
            )
    return grid


def shuffled_baseline(rows: List[dict], *, seed: int, rounds: int) -> Dict[str, object]:
    rng = random.Random(seed)
    actions = [r.get("action", "") for r in rows]
    directions = [r.get("position_direction", "") for r in rows]
    hold_bars = [as_int(r, "hold_bars") for r in rows]
    collisions = []
    action_entropy = []

    for _ in range(rounds):
        shuffled_actions = actions[:]
        shuffled_dirs = directions[:]
        rng.shuffle(shuffled_actions)
        rng.shuffle(shuffled_dirs)
        collisions.append(sum(1 for a, d in zip(shuffled_actions, shuffled_dirs) if a == "enter" and d == "flat"))
        counts = Counter(shuffled_actions)
        total = max(1, len(shuffled_actions))
        entropy = 0.0
        for count in counts.values():
            p = count / total
            entropy -= 0.0 if p <= 0.0 else p * math.log(p, 2)
        action_entropy.append(entropy)

    return {
        "rounds": rounds,
        "seed": seed,
        "avg_shuffled_enter_flat_collisions": mean(collisions) if collisions else 0.0,
        "avg_shuffled_action_entropy": mean(action_entropy) if action_entropy else 0.0,
        "avg_hold_bars_reference": mean(hold_bars) if hold_bars else 0.0,
    }


def family_groups(rows: List[dict]) -> Dict[str, dict]:
    groups: Dict[str, List[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get("family_name", "unknown")].append(row)
    return {family: {"rows": len(rs), "actions": dict(Counter(r.get("action", "") for r in rs))} for family, rs in groups.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal", required=True, help="Path to paper journal CSV")
    ap.add_argument("--out-json", default="", help="Optional JSON report output path")
    ap.add_argument("--entry-threshold", type=float, default=68.0)
    ap.add_argument("--exit-threshold", type=float, default=60.0)
    ap.add_argument("--shuffle-rounds", type=int, default=200)
    ap.add_argument("--shuffle-seed", type=int, default=13)
    args = ap.parse_args()

    rows = load_rows(Path(args.journal))
    report = {
        "summary": summarize(rows, entry_threshold=args.entry_threshold, exit_threshold=args.exit_threshold),
        "threshold_grid": threshold_grid(rows, [58.0, 62.0, 68.0, 74.0], [48.0, 54.0, 60.0, 66.0]),
        "shuffled_baseline": shuffled_baseline(rows, seed=args.shuffle_seed, rounds=args.shuffle_rounds),
        "families": family_groups(rows),
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
