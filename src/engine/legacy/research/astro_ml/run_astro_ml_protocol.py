#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from astro_ml_core import DEFAULT_COMMON_FILES, ensure_dir, read_csv_flexible, save_excel, save_json, stable_run_id

THIS = Path(__file__).resolve().parent


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_cmd(args: List[str], cwd: Optional[Path] = None) -> str:
    print("\n>>> " + " ".join(str(a) for a in args))
    proc = subprocess.run(args, cwd=str(cwd or THIS), text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc.stdout or ""


def grab(stdout: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}=(.+)$", stdout, flags=re.MULTILINE)
    return m.group(1).strip() if m else ""


def resolve_common_path(path_text: str, common: Path) -> Path:
    p = Path(path_text)
    return p if p.is_absolute() else common / p


def parse_targets(raw: str, horizons: List[int], preset: str) -> List[str]:
    if raw.strip():
        return [x.strip() for x in raw.split(",") if x.strip()]
    if preset == "direction_only":
        return [f"label_direction_{h}" for h in horizons]
    if preset == "sanity":
        h = horizons[min(1, len(horizons)-1)] if horizons else 60
        return [f"label_direction_{h}", f"label_spike_{h}", f"label_bull_trap_{h}"]
    # professional default
    mid = horizons[min(1, len(horizons)-1)] if horizons else 60
    out = []
    for h in horizons:
        out.append(f"label_direction_{h}")
    out += [
        f"label_clean_long_{mid}",
        f"label_clean_short_{mid}",
        f"label_spike_{mid}",
        f"label_bull_trap_{mid}",
        f"label_bear_trap_{mid}",
    ]
    return list(dict.fromkeys(out))


def safe_rel_to_common(p: Path, common: Path) -> str:
    try:
        return str(p.relative_to(common))
    except Exception:
        return str(p)


def main() -> int:
    ap = argparse.ArgumentParser(description="One-command EXP0016 professional Astro ML protocol runner.")
    ap.add_argument("--astro-csv", required=True, help="Astro feature CSV name in Common Files or absolute path.")
    ap.add_argument("--price-csv", default="", help="Price CSV name in Common Files or absolute path.")
    ap.add_argument("--asset", default="NAS100")
    ap.add_argument("--timeframe", default="M1")
    ap.add_argument("--common-files", default=str(DEFAULT_COMMON_FILES))
    ap.add_argument("--horizons", default="30,60,120")
    ap.add_argument("--preset", choices=["sanity", "direction_only", "professional"], default="professional")
    ap.add_argument("--targets", default="", help="Comma-separated target override.")
    ap.add_argument("--model-type", choices=["extra_trees", "random_forest", "gradient_boosting", "logit"], default="extra_trees")
    ap.add_argument("--test-fraction", type=float, default=0.25)
    ap.add_argument("--n-estimators", type=int, default=700)
    ap.add_argument("--max-depth", type=int, default=10)
    ap.add_argument("--run-walk-forward", action="store_true")
    ap.add_argument("--train-days", type=int, default=120)
    ap.add_argument("--test-days", type=int, default=20)
    ap.add_argument("--step-days", type=int, default=20)
    ap.add_argument("--embargo-bars", type=int, default=120)
    ap.add_argument("--direction-threshold-pct", type=float, default=0.0010)
    ap.add_argument("--spike-threshold-pct", type=float, default=0.0030)
    ap.add_argument("--trap-trigger-pct", type=float, default=0.0015)
    ap.add_argument("--clean-min-mfe-pct", type=float, default=0.0015)
    ap.add_argument("--clean-max-mae-pct", type=float, default=0.0008)
    ap.add_argument("--allow-audit-warnings", action="store_true", help="Do not fail the protocol on critical dataset-audit gates.")
    ap.add_argument("--audit-min-rows", type=int, default=0, help="Override minimum dataset rows for the audit gate.")
    args = ap.parse_args()

    common = Path(args.common_files)
    horizons = [int(x.strip()) for x in args.horizons.split(",") if x.strip()]
    protocol_id = f"{now_id()}_{stable_run_id([args.asset, args.timeframe, args.astro_csv, args.price_csv, args.preset])}"
    proto_dir = common / "astro_ml" / "protocol_runs" / args.asset / args.timeframe / protocol_id
    ensure_dir(proto_dir)

    dataset_name = f"astro_ml_dataset_{args.asset}_{args.timeframe}_{protocol_id}.csv"
    dataset_rel_path = Path("astro_ml") / "reports" / args.asset / args.timeframe / dataset_name
    dataset_abs = common / dataset_rel_path
    xlsx_abs = dataset_abs.with_suffix(".xlsx")

    manifest: Dict[str, object] = {
        "protocol_id": protocol_id,
        "asset": args.asset,
        "timeframe": args.timeframe,
        "preset": args.preset,
        "astro_csv": args.astro_csv,
        "price_csv": args.price_csv,
        "horizons": horizons,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_dir": str(proto_dir),
        "dataset_csv": str(dataset_abs),
        "runs": [],
        "walk_forward": [],
    }

    # 1) Build dataset
    build_cmd = [
        sys.executable, str(THIS / "build_astro_ml_dataset.py"),
        "--astro-csv", args.astro_csv,
        "--asset", args.asset,
        "--timeframe", args.timeframe,
        "--common-files", str(common),
        "--out-csv", str(dataset_abs),
        "--out-xlsx", str(xlsx_abs),
        "--horizons", args.horizons,
        "--direction-threshold-pct", str(args.direction_threshold_pct),
        "--spike-threshold-pct", str(args.spike_threshold_pct),
        "--trap-trigger-pct", str(args.trap_trigger_pct),
        "--clean-min-mfe-pct", str(args.clean_min_mfe_pct),
        "--clean-max-mae-pct", str(args.clean_max_mae_pct),
    ]
    if args.price_csv:
        build_cmd += ["--price-csv", args.price_csv]
    out = run_cmd(build_cmd)
    dataset_path = Path(grab(out, "ASTRO_ML_DATASET_CSV") or str(dataset_abs))
    manifest["dataset_csv"] = str(dataset_path)
    manifest["dataset_xlsx"] = str(xlsx_abs)

    # 2) Audit dataset
    audit_min_rows = args.audit_min_rows
    if audit_min_rows <= 0:
        audit_min_rows = 10000 if args.preset == "professional" else 1000
    audit_cmd = [
        sys.executable, str(THIS / "astro_ml_audit_dataset.py"),
        "--dataset-csv", str(dataset_path),
        "--asset", args.asset,
        "--timeframe", args.timeframe,
        "--common-files", str(common),
        "--out-xlsx", str(proto_dir / "dataset_audit.xlsx"),
        "--out-json", str(proto_dir / "dataset_audit.json"),
        "--min-rows", str(audit_min_rows),
    ]
    if args.preset == "professional" and not args.allow_audit_warnings:
        audit_cmd.append("--fail-on-critical")
    audit_out = run_cmd(audit_cmd)
    manifest["dataset_audit_xlsx"] = grab(audit_out, "ASTRO_ML_AUDIT_XLSX")
    manifest["dataset_audit_json"] = str(proto_dir / "dataset_audit.json")
    manifest["audit_min_rows"] = audit_min_rows
    manifest["audit_fail_on_critical"] = bool(args.preset == "professional" and not args.allow_audit_warnings)

    df = read_csv_flexible(dataset_path, max_rows=10)
    available = set(df.columns)
    targets = [t for t in parse_targets(args.targets, horizons, args.preset) if t in available]
    skipped = [t for t in parse_targets(args.targets, horizons, args.preset) if t not in available]
    manifest["targets_requested"] = parse_targets(args.targets, horizons, args.preset)
    manifest["targets_trained"] = targets
    manifest["targets_skipped_missing"] = skipped
    if not targets:
        raise SystemExit("No requested targets exist in dataset. Check horizons/labels.")

    # 3) Train model suite
    for target in targets:
        train_out = run_cmd([
            sys.executable, str(THIS / "train_astro_meta_learner.py"),
            "--dataset-csv", str(dataset_path),
            "--target", target,
            "--asset", args.asset,
            "--timeframe", args.timeframe,
            "--common-files", str(common),
            "--model-type", args.model_type,
            "--test-fraction", str(args.test_fraction),
            "--n-estimators", str(args.n_estimators),
            "--max-depth", str(args.max_depth),
        ])
        run_id = grab(train_out, "ASTRO_ML_RUN_ID")
        run_dir = grab(train_out, "ASTRO_ML_RUN_DIR")
        acc = grab(train_out, "ACCURACY")
        card_out = ""
        if run_dir:
            card_out = run_cmd([sys.executable, str(THIS / "make_astro_model_card.py"), "--run-dir", run_dir])
        manifest["runs"].append({"target": target, "run_id": run_id, "run_dir": run_dir, "train_stdout_accuracy_line": acc, "model_card": grab(card_out, "ASTRO_ML_MODEL_CARD_MD")})

        if args.run_walk_forward:
            wf_out = run_cmd([
                sys.executable, str(THIS / "evaluate_walk_forward.py"),
                "--dataset-csv", str(dataset_path),
                "--target", target,
                "--asset", args.asset,
                "--timeframe", args.timeframe,
                "--common-files", str(common),
                "--train-days", str(args.train_days),
                "--test-days", str(args.test_days),
                "--step-days", str(args.step_days),
                "--embargo-bars", str(args.embargo_bars),
                "--model-type", args.model_type,
            ])
            manifest["walk_forward"].append({"target": target, "stdout": wf_out[-4000:]})

    # 4) Export accumulated knowledge pack
    kp_out = run_cmd([
        sys.executable, str(THIS / "export_astro_knowledge_pack.py"),
        "--asset", args.asset,
        "--timeframe", args.timeframe,
        "--common-files", str(common),
    ])
    manifest["knowledge_pack_json"] = grab(kp_out, "ASTRO_KNOWLEDGE_PACK_JSON")
    manifest["knowledge_pack_md"] = grab(kp_out, "ASTRO_KNOWLEDGE_PACK_MD")

    save_json(proto_dir / "protocol_manifest.json", manifest)

    rows = []
    for r in manifest["runs"]:  # type: ignore[index]
        rows.append(r)
    save_excel(proto_dir / "protocol_report.xlsx", {
        "Manifest": pd.DataFrame([{k: v for k, v in manifest.items() if k not in ("runs", "walk_forward")}]),
        "Runs": pd.DataFrame(rows),
        "WalkForward": pd.DataFrame(manifest.get("walk_forward", [])),
    })

    md = [f"# Astro ML Protocol Run - {protocol_id}\n"]
    md.append(f"Asset: `{args.asset}`  Timeframe: `{args.timeframe}`  Preset: `{args.preset}`\n")
    md.append(f"Dataset: `{dataset_path}`\n")
    md.append("## Trained targets\n")
    for r in manifest["runs"]:  # type: ignore[index]
        md.append(f"- `{r['target']}` run=`{r['run_id']}` card=`{r.get('model_card','')}`")
    if skipped:
        md.append("\n## Skipped missing targets\n")
        for s in skipped:
            md.append(f"- `{s}`")
    md.append(f"\nKnowledge pack: `{manifest.get('knowledge_pack_md','')}`\n")
    (proto_dir / "PROTOCOL_REPORT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"ASTRO_ML_PROTOCOL_ID={protocol_id}")
    print(f"ASTRO_ML_PROTOCOL_DIR={proto_dir}")
    print(f"ASTRO_ML_PROTOCOL_REPORT={proto_dir / 'PROTOCOL_REPORT.md'}")
    print(f"ASTRO_ML_PROTOCOL_XLSX={proto_dir / 'protocol_report.xlsx'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
