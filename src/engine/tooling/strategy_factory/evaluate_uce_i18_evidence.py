#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path
import time

from strategy_factory_qualification_v3.evidence import build_evidence_bundle
from strategy_factory_qualification_v3.enums import ReleaseStage
from strategy_factory_qualification_v3.parsing import (
    parse_chaos,
    parse_compile,
    parse_differential,
    parse_environment,
    parse_policy,
    parse_recovery,
    parse_rollback,
    parse_security,
    parse_soak,
    parse_stage,
)
from strategy_factory_qualification_v3.qualification import qualify


def load(path: Path) -> dict:
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError(f"evidence file exceeds 16 MiB: {path}")
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"evidence file must contain an object: {path}")
    return value


def optional(root: Path, name: str, parser):
    path = root / name
    return parser(load(path)) if path.exists() else None


def jsonable(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a frozen UCE-I18 external evidence directory")
    parser.add_argument("evidence_directory")
    parser.add_argument("--output-directory", default="")
    args = parser.parse_args()
    root = Path(args.evidence_directory).resolve()
    claims = load(root / "claims.json")
    requested_stage = ReleaseStage(claims["requested_stage"])
    evaluated_at_ms = int(claims.get("evaluated_at_ms", time.time_ns() // 1_000_000))
    report = qualify(
        policy=parse_policy(load(root / "policy.json")),
        environment=parse_environment(load(root / "environment.json")),
        source_commit=str(claims["source_commit"]),
        evaluated_at_ms=evaluated_at_ms,
        requested_stage=requested_stage,
        compile_evidence=optional(root, "compile.json", parse_compile),
        parity_report=optional(root, "parity.json", parse_differential),
        tester_report=optional(root, "tester.json", parse_differential),
        soak_report=optional(root, "soak.json", parse_soak),
        chaos_report=optional(root, "chaos.json", parse_chaos),
        recovery_report=optional(root, "recovery.json", parse_recovery),
        security_report=optional(root, "security.json", parse_security),
        paper_evidence=optional(root, "paper.json", parse_stage),
        shadow_evidence=optional(root, "shadow.json", parse_stage),
        micro_live_evidence=optional(root, "micro_live.json", parse_stage),
        limited_live_evidence=optional(root, "limited_live.json", parse_stage),
        production_evidence=optional(root, "production.json", parse_stage),
        rollback_report=optional(root, "rollback.json", parse_rollback),
        source_integrity_passed=bool(claims.get("source_integrity_passed", False)),
        source_integrity_evidence_hash=str(claims.get("source_integrity_evidence_hash", "")),
        broker_reconciliation_passed=bool(claims.get("broker_reconciliation_passed", False)),
        broker_reconciliation_evidence_hash=str(claims.get("broker_reconciliation_evidence_hash", "")),
        human_approval_id=str(claims.get("human_approval_id", "")),
        human_approval_evidence_hash=str(claims.get("human_approval_evidence_hash", "")),
        limitations=tuple(claims.get("limitations", ())),
    )
    hashes = {}
    for path in sorted(root.glob("*.json")):
        import hashlib
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    bundle = build_evidence_bundle(report, hashes, external_evidence_present=True)
    out = Path(args.output_directory).resolve() if args.output_directory else root / "evaluation"
    out.mkdir(parents=True, exist_ok=True)
    (out / "qualification_report.json").write_text(json.dumps(jsonable(asdict(report)), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "evidence_bundle.json").write_text(json.dumps(jsonable(bundle), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0 if report.decision.value == "qualified" else 2


if __name__ == "__main__":
    raise SystemExit(main())
