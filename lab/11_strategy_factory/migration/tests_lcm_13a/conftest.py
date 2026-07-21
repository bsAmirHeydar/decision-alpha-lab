from __future__ import annotations
import json
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[4]
DUAL_ROOT = REPO / "registry/legacy_context_migration/dual_run_evidence/DUALRUN_7302C947E4F606482E1D09A8FF069570"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

@pytest.fixture(scope="session")
def dual_root():
    return DUAL_ROOT

@pytest.fixture(scope="session")
def consumers(dual_root):
    return load_jsonl(dual_root / "records/exact_consumer_inventory.jsonl")

@pytest.fixture(scope="session")
def scenarios(dual_root):
    return load_jsonl(dual_root / "records/dual_run_scenarios.jsonl")

@pytest.fixture(scope="session")
def results(dual_root):
    return load_jsonl(dual_root / "records/dual_run_results.jsonl")

@pytest.fixture(scope="session")
def mismatches(dual_root):
    return load_jsonl(dual_root / "mismatch_registry.jsonl")

@pytest.fixture(scope="session")
def eligibility(dual_root):
    return load_jsonl(dual_root / "records/consumer_eligibility_records.jsonl")
