from __future__ import annotations

import json
from pathlib import Path


def validate(repo_root):
    repo_root = Path(repo_root)
    policies = sorted((repo_root / "registry/legacy_context_migration/lcm_06/policies").glob("*.json"))
    parsed = [json.loads(path.read_text(encoding="utf-8")) for path in policies]
    forbidden: list[dict] = []

    source_roots = [
        repo_root / "src/engine/tooling/strategy_factory/lcm/lcm_06",
        repo_root / "mql5/legacy/strategy_factory_lab/Include/AlphaLab/ContextOS/Migration/LCM06",
    ]
    forbidden_tokens = (
        "OrderSend(",
        "CTrade",
        "PositionOpen(",
        "PositionModify(",
        "PositionClose(",
        "WebRequest(",
        "subprocess.Popen(",
        "shell=True",
        "os.system(",
        "eval(",
        "exec(",
    )
    for source_root in source_roots:
        if not source_root.is_dir():
            continue
        for path in sorted(item for item in source_root.rglob("*") if item.is_file() and item.suffix.lower() in {".py", ".mqh", ".mq5"}):
            if path.name == "static_validation.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden_tokens:
                if token in text:
                    forbidden.append({"path": path.relative_to(repo_root).as_posix(), "token": token})

    bad_phase = [item.get("policy_id") for item in parsed if item.get("phase_id") != "LCM-06"]
    bad_claim = [item.get("policy_id") for item in parsed if item.get("claim_ceiling") not in (None, "MIGRATION_FRAMEWORK_REFERENCE_ONLY")]
    open_policies = [item.get("policy_id") for item in parsed if item.get("closed") is not True]
    authority_findings = []
    for item in parsed:
        rules = item.get("rules", {}) if isinstance(item.get("rules"), dict) else {}
        for key in (
            "source_move_allowed",
            "source_delete_allowed",
            "target_materialization_allowed",
            "semantic_refactor_allowed",
            "merge_allowed",
            "cutover_allowed",
            "runtime_authority",
            "live_order_authority",
            "capital_authority",
        ):
            if item.get(key) is True or rules.get(key) is True:
                authority_findings.append({"policy_id": item.get("policy_id"), "field": key})

    return {
        "passed": not forbidden and not bad_phase and not bad_claim and not open_policies and not authority_findings,
        "policy_count": len(policies),
        "forbidden_findings": forbidden,
        "bad_policy_phase_ids": bad_phase,
        "bad_claim_ceilings": bad_claim,
        "open_policies": open_policies,
        "authority_findings": authority_findings,
    }
