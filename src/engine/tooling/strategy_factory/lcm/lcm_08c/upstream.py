from __future__ import annotations
from pathlib import Path
from .canonical import file_digest
from .errors import UpstreamBindingError
from .io import load_json, load_jsonl

PORTFOLIO_ID = "CTXPORT_B9FA4843859B2E2A1EBD37E4167705E1"
PILOT_ID = "CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1"
EXPECTED_LCM08B_HANDOFF = "sha256:c5695d5a671b09723851df4989a8a617242b5a2a7518885040cfb0b986451381"

def load_upstream(repo_root: Path) -> dict:
    portfolio_root = repo_root / "registry/history/lcm/context_portfolios/CTXPORT_B9FA4843859B2E2A1EBD37E4167705E1"
    pilot_root = repo_root / "registry/history/lcm/pilot_migrations/PILOTMIG_344455420C8CA68E865FD54135E891D7"
    rows = load_jsonl(portfolio_root / "portfolio/context_portfolio_registry.jsonl")
    assignment = load_json(portfolio_root / "waves/context_wave_assignment.json")
    summary = load_json(portfolio_root / "reports/context_portfolio_summary.json")
    handoff = load_json(pilot_root / "handoff/lcm08b_to_lcm08c_handoff.json")
    parity = load_json(pilot_root / "parity/parity_report.json")
    acceptance = load_json(pilot_root / "reports/acceptance_report.json")
    if handoff.get("handoff_digest") != EXPECTED_LCM08B_HANDOFF:
        raise UpstreamBindingError("LCM-08B handoff digest mismatch")
    if len(rows) != summary.get("context_candidate_count"):
        raise UpstreamBindingError("portfolio count mismatch")
    if not parity.get("hard_parity_passed") or not acceptance.get("acceptance_gate_passed"):
        raise UpstreamBindingError("pilot acceptance/parity not valid")
    for row in rows:
        path = repo_root / row["source_artifact_path"]
        if not path.is_file() or file_digest(path) != row["source_artifact_sha256"]:
            raise UpstreamBindingError(f"source lock mismatch: {row['identity_id']}")
    return {"portfolio_rows": rows, "wave_assignment": assignment, "summary": summary, "handoff": handoff, "parity": parity, "acceptance": acceptance}
