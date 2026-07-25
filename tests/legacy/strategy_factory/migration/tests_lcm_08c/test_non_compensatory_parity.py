from tools.repository_paths import find_repository_root
from pathlib import Path
import json

REPO = find_repository_root(__file__)
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"
PILOT = "CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1"

def rows(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x.strip()]

def test_only_pilot_is_parity_passed_and_cutover_ready():
    parity = rows("registries/context_parity_registry.jsonl")
    packages = rows("registries/context_package_registry.jsonl")
    assert [x["identity_id"] for x in parity if x["hard_parity_passed"]] == [PILOT]
    assert [x["identity_id"] for x in packages if x["cutover_ready"]] == [PILOT]
    assert all(x["parity_state"] == "NOT_EXECUTED_BLOCKED" for x in parity if x["identity_id"] != PILOT)

def test_wave_receipts_are_non_compensatory_and_accounted():
    receipts = [json.loads(p.read_text()) for p in (ROOT / "wave_admission_receipts").glob("*.json")]
    assert len(receipts) == 6
    assert all(x["all_members_accounted"] and x["non_compensatory_gate_passed"] for x in receipts)
    assert sum(x["member_count"] for x in receipts) == 321
