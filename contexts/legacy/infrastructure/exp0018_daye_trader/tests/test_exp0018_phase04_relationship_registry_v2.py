from __future__ import annotations
from tools.repository_paths import find_repository_root

import csv
import importlib.util
import json
from pathlib import Path

ROOT = find_repository_root(__file__)
VALIDATOR = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase04_relationship_registry_v2.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("p04_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_validator_passes():
    module = load_validator()
    assert module.validate(ROOT) == []


def test_registry_cardinality_and_blockers():
    path = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_relationship_registry_contract_v2.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["relationships"]
    assert len(rows) == 22
    assert sum(bool(r["major"]) for r in rows) == 6
    assert sum(not bool(r["major"]) for r in rows) == 16
    blocked = {r["source_alias"]: r["blocker_decision_id"] for r in rows if not r["implementation_ready"]}
    assert blocked == {"WW": "DY-A03", "NP": "DY-A05"}


def test_registry_chain_is_canonical():
    path = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_relationship_registry_v2.csv"
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = {r["source_alias"]: r for r in csv.DictReader(f)}
    assert rows["PA"]["current_period_code"] == "A"
    assert rows["PA"]["reference_period_code"] == "P"
    assert rows["p4a1"]["current_period_code"] == "a1"
    assert rows["p4a1"]["reference_period_code"] == "p4"
    assert rows["p3p4"]["current_period_code"] == "p4"
    assert rows["p3p4"]["reference_period_code"] == "p3"


def test_fixture_has_fail_closed_cases():
    path = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_relationship_resolution_cases_v2.csv"
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    statuses = {r["expected_status"] for r in rows}
    assert "REFERENCE_NOT_COMPLETE" in statuses
    assert "CURRENT_NOT_ELIGIBLE" in statuses
    assert "REFERENCE_CODE_MISMATCH" in statuses
