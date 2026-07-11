from __future__ import annotations
from dataclasses import asdict
from enum import IntEnum
from pathlib import Path
import json

def _plain(value):
    if isinstance(value, IntEnum):return int(value)
    if isinstance(value, tuple):return [_plain(v) for v in value]
    if isinstance(value, list):return [_plain(v) for v in value]
    if isinstance(value, dict):return {k:_plain(v) for k,v in value.items()}
    if hasattr(value,"__dataclass_fields__"):return _plain(asdict(value))
    return value

def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(_plain(value),indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_jsonl(path: Path, values) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="\n") as handle:
        for value in values:handle.write(json.dumps(_plain(value),sort_keys=True,separators=(",",":"))+"\n")

def write_governance_bundle(directory: Path, *, evidence, evaluation, registry, snapshot,
                            release_manifest=None, rollback_plan=None, report_manifest=None) -> None:
    write_json(directory/"model_evidence_bundle.json",evidence)
    write_json(directory/"promotion_evaluation.json",evaluation)
    write_jsonl(directory/"governance_decisions.jsonl",registry.ledger.decisions)
    write_json(directory/"registry_snapshot.json",snapshot)
    if release_manifest is not None:write_json(directory/"model_release_manifest.json",release_manifest)
    if rollback_plan is not None:write_json(directory/"rollback_plan.json",rollback_plan)
    if report_manifest is not None:write_json(directory/"governance_report_manifest.json",report_manifest)
