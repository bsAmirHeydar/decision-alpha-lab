from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from src.engine.tooling.strategy_factory.lcm.lcm_08c.schema_validation import validate_schema_directory

REPO = find_repository_root(__file__)
ROOT = REPO / "registry/history/lcm/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def test_all_schemas_are_valid_draft_2020_12():
    out = validate_schema_directory(REPO / "registry/history/lcm/lcm_08c/schemas/v1")
    assert out["passed"] and out["schema_count"] == 14

def test_hostile_review_and_acceptance_pass():
    hostile = json.loads((ROOT / "reports/hostile_review.json").read_text())
    acceptance = json.loads((ROOT / "reports/acceptance_report.json").read_text())
    assert hostile["hostile_review_passed"] and hostile["failed_check_count"] == 0
    assert acceptance["acceptance_gate_passed"]
