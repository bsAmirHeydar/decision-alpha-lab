from __future__ import annotations
from typing import Any
from .authority import OUTPUT_AUTHORITY, validate_handoff
from .canonical import content_hash, stable_id
from .errors import BudgetError, ContractError, IntegrityError
from .exposure import build_exposure_ledger
from .models import ExecutionTwinProfile
from .scenario import simulate_scenario
from .version import PHASE, VERSION


def _validate_source_rows(cube: dict[str, Any]) -> list[dict[str, Any]]:
    rows = list(cube.get("rows", []))
    if len(rows) != int(cube.get("row_count", -1)):
        raise IntegrityError("source cube row count mismatch")
    ids = [r.get("row_id") for r in rows]
    hashes = [r.get("row_hash") for r in rows]
    if any(not v for v in ids + hashes) or len(set(ids)) != len(ids):
        raise IntegrityError("source row identity is missing or duplicated")
    return sorted(rows, key=lambda r: r["row_id"])


def build_execution_twin(cube: dict[str, Any], handoff: dict[str, Any], profile: ExecutionTwinProfile) -> dict[str, Any]:
    validate_handoff(cube, handoff)
    rows = _validate_source_rows(cube)
    if cube.get("evidence_role") not in profile.allowed_evidence_roles:
        raise ContractError("source evidence role is not allowed by profile")
    if len(rows) > profile.maximum_source_rows:
        raise BudgetError("source row budget exceeded")
    scenarios = sorted(profile.scenarios, key=lambda s: s.scenario_id)
    if len(scenarios) > profile.maximum_scenarios:
        raise BudgetError("scenario budget exceeded")
    twin_rows = [simulate_scenario(row, cube, profile, scenario) for row in rows for scenario in scenarios]
    twin_rows.sort(key=lambda r: (r["source_row_id"], r["scenario_id"]))
    ledger = build_exposure_ledger(rows, scenarios, twin_rows)
    if not ledger["complete"]:
        raise IntegrityError("execution twin exposure is incomplete")
    payload = {
        "phase": PHASE, "version": VERSION, "source_cube_id": cube["cube_id"], "source_cube_hash": cube["cube_hash"],
        "source_handoff_id": handoff["handoff_id"], "source_handoff_hash": handoff["handoff_hash"],
        "profile_id": profile.profile_id, "profile_hash": profile.profile_hash, "evidence_class": profile.evidence_class,
        "synthetic_watermark": profile.synthetic_watermark, "evidence_role": cube["evidence_role"], "known_as_of": cube["known_as_of"],
        "decision_time_ms": cube["decision_time_ms"], "source_row_count": len(rows), "scenario_count": len(scenarios), "twin_row_count": len(twin_rows),
        "complete_exposure": True, "authority": OUTPUT_AUTHORITY, "ranking_semantics": "none", "shadow_replacement": False,
        "calibration_claim": profile.evidence_class != "reference_synthetic", "scenarios": [s.semantic_payload() | {"scenario_hash": s.scenario_hash} for s in scenarios],
        "rows": twin_rows, "exposure_ledger": ledger,
        "limitations": [
            "V4-09 is a descriptive and stress execution digital twin, not an order router.",
            "Reference-synthetic outputs cannot provide positive promotion evidence.",
            "The execution digital twin does not replace prospective paper, shadow, broker qualification, or UCEE I18 release evidence.",
            "No treatment ranking, selection, risk allocation, runtime activation, or order authority is present.",
        ],
    }
    payload["twin_id"] = stable_id("executiontwin", payload); payload["twin_hash"] = content_hash(payload)
    return payload
