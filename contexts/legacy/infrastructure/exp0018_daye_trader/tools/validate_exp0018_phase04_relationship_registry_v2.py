from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

EXPECTED = {
    "WW": ("DAYE_W_CURR_VS_W_PREV", "W", "W", "PREVIOUS_SAME_CODE", False, "DY-A03"),
    "DD": ("DAYE_D_CURR_VS_D_PREV", "D", "D", "PREVIOUS_SAME_CODE", True, ""),
    "PA": ("DAYE_A_CURR_VS_P_PREV", "A", "P", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "AL": ("DAYE_L_CURR_VS_A_PREV", "L", "A", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "LN": ("DAYE_N_CURR_VS_L_PREV", "N", "L", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "NP": ("DAYE_P_CURR_VS_N_PREV", "P", "N", "PREVIOUS_CHRONOLOGICAL", False, "DY-A05"),
    "p4a1": ("DAYE_A1_VS_P4", "a1", "p4", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "a1a2": ("DAYE_A2_VS_A1", "a2", "a1", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "a2a3": ("DAYE_A3_VS_A2", "a3", "a2", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "a3a4": ("DAYE_A4_VS_A3", "a4", "a3", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "a4l1": ("DAYE_L1_VS_A4", "l1", "a4", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "l1l2": ("DAYE_L2_VS_L1", "l2", "l1", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "l2l3": ("DAYE_L3_VS_L2", "l3", "l2", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "l3l4": ("DAYE_L4_VS_L3", "l4", "l3", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "l4n1": ("DAYE_N1_VS_L4", "n1", "l4", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "n1n2": ("DAYE_N2_VS_N1", "n2", "n1", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "n2n3": ("DAYE_N3_VS_N2", "n3", "n2", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "n3n4": ("DAYE_N4_VS_N3", "n4", "n3", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "n4p1": ("DAYE_P1_VS_N4", "p1", "n4", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "p1p2": ("DAYE_P2_VS_P1", "p2", "p1", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "p2p3": ("DAYE_P3_VS_P2", "p3", "p2", "PREVIOUS_CHRONOLOGICAL", True, ""),
    "p3p4": ("DAYE_P4_VS_P3", "p4", "p3", "PREVIOUS_CHRONOLOGICAL", True, ""),
}

FORBIDDEN = ["OrderSend", "CTrade", "PositionOpen", "WebRequest", "LongToString"]


def validate(repo: Path) -> list[str]:
    errors: list[str] = []
    contract_path = repo / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_relationship_registry_contract_v2.json"
    csv_path = repo / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_relationship_registry_v2.csv"
    fixture_path = repo / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_relationship_resolution_cases_v2.csv"
    mql_dir = repo / "mql5/Include/DayeTrader/EXP0018"
    expert = repo / "mql5/Experts/DayeTrader/EXP0018_Daye_Relationship_Registry_Anatomy.mq5"

    for p in [contract_path, csv_path, fixture_path, expert]:
        if not p.exists():
            errors.append(f"missing required file: {p}")
    if errors:
        return errors

    data = json.loads(contract_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2:
        errors.append("contract schema_version must be 2")
    if data.get("execution_authority") is not False:
        errors.append("execution_authority must be false")
    rels = data.get("relationships", [])
    if len(rels) != 22:
        errors.append(f"expected 22 relationships, got {len(rels)}")
    major = sum(bool(r.get("major")) for r in rels)
    if major != 6:
        errors.append(f"expected 6 major relationships, got {major}")
    if len(rels) - major != 16:
        errors.append(f"expected 16 minor relationships, got {len(rels)-major}")
    blocked = [r for r in rels if not r.get("implementation_ready")]
    if len(blocked) != 2:
        errors.append(f"expected 2 blocked relationships, got {len(blocked)}")

    aliases = [r.get("source_alias") for r in rels]
    ids = [r.get("relationship_id") for r in rels]
    if len(set(aliases)) != len(aliases):
        errors.append("duplicate source_alias detected")
    if len(set(ids)) != len(ids):
        errors.append("duplicate relationship_id detected")

    by_alias = {r["source_alias"]: r for r in rels}
    if set(by_alias) != set(EXPECTED):
        errors.append("relationship alias set differs from canonical 22")
    for alias, expected in EXPECTED.items():
        row = by_alias.get(alias)
        if not row:
            continue
        rid, cur, ref, selector, ready, blocker = expected
        actual = (
            row.get("relationship_id"), row.get("current_period_code"),
            row.get("reference_period_code"), row.get("selector"),
            bool(row.get("implementation_ready")), row.get("blocker_decision_id", "")
        )
        if actual != expected:
            errors.append(f"mapping mismatch for {alias}: expected={expected} actual={actual}")

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        csv_rows = list(csv.DictReader(f))
    if len(csv_rows) != 22:
        errors.append(f"registry CSV must contain 22 rows, got {len(csv_rows)}")

    with fixture_path.open(encoding="utf-8-sig", newline="") as f:
        fixture_rows = list(csv.DictReader(f))
    required_statuses = {"READY", "BLOCKED_BY_DOCTRINE", "REFERENCE_NOT_COMPLETE", "CURRENT_NOT_ELIGIBLE", "REFERENCE_CODE_MISMATCH"}
    actual_statuses = {r["expected_status"] for r in fixture_rows}
    if not required_statuses.issubset(actual_statuses):
        errors.append("fixture catalog does not cover all required status classes")

    phase_files = [expert] + sorted(mql_dir.glob("DAYE_Relationship*.mqh"))
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in phase_files)
    for token in FORBIDDEN:
        if token in text:
            errors.append(f"forbidden token found in Phase04 MQL5: {token}")
    if re.search(r"=\s*StringTo(?:Upper|Lower)\s*\(", text):
        errors.append("invalid MQL5 StringToUpper/StringToLower assignment pattern found")
    if "22-Relationship" not in text and "22-relationship" not in text:
        errors.append("Phase04 code does not declare the 22-relationship boundary")

    docs = repo / "docs/operations/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/11_phase04_relationship_registry_v2"
    if not docs.exists():
        errors.append("Phase04 documentation directory missing")
    else:
        md_count = len(list(docs.glob("*.md")))
        if md_count < 20:
            errors.append(f"expected at least 20 Phase04 docs, got {md_count}")

    moc = repo / "docs/history/obsidian/deep/00_mocs/CG_EXP0018_PHASE04_RELATIONSHIP_REGISTRY_MOC.md"
    if not moc.exists():
        errors.append("Phase04 deep Obsidian MOC missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    errors = validate(repo)
    if errors:
        print("EXP0018 Phase04 relationship registry validation: FAIL")
        for err in errors:
            print(f"ERROR: {err}")
        return 1
    print("EXP0018 Phase04 relationship registry validation: PASS")
    print("relationships=22 major=6 minor=16 ready=20 blocked=2")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
