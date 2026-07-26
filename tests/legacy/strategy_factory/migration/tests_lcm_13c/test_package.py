import json

from src.engine.tooling.strategy_factory.lcm.lcm_13c.canonical import verify_embedded_digest
from src.engine.tooling.strategy_factory.lcm.lcm_13c.constants import EVENT_TYPES, STATE_PLANES
from src.engine.tooling.strategy_factory.lcm.lcm_13c.io import iter_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_13c.verify import verify_package


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_package_verifies(built):
    assert verify_package(built) == []


def test_closure_counts(built):
    registry = load(built / "cutover_closure_registry.json")
    assert registry["wave_count"] == 27
    assert registry["consumer_count"] == 613
    assert registry["closure_counts"] == {
        "CLOSED": 0,
        "CLOSED_WITH_RESIDUAL_RISK": 27,
        "REOPEN_REQUIRED": 0,
    }


def test_state_plane_accounting(built):
    rows = list(iter_jsonl(built / "records/state_recovery_records.jsonl"))
    assert len(rows) == 27 * len(STATE_PLANES) == 162
    assert {row["state_plane"] for row in rows} == set(STATE_PLANES)
    assert all(row["live_state_mutation_performed"] is False for row in rows)


def test_event_ledger_complete(built):
    rows = list(iter_jsonl(built / "closure_event_ledger.jsonl"))
    assert len(rows) == 27 * len(EVENT_TYPES) == 189
    assert [row["event_sequence"] for row in rows] == list(range(1, 190))
    assert {row["event_type"] for row in rows} == set(EVENT_TYPES)


def test_deprecation_candidates_exact(built):
    rows = list(iter_jsonl(built / "records/deprecation_candidate_records.jsonl"))
    assert len(rows) == 613
    assert len({row["consumer_id"] for row in rows}) == 613
    assert all(verify_embedded_digest(row, "candidate_digest") for row in rows)
    assert all(row["quarantine_authorized"] is False for row in rows)
    assert all(row["deletion_authorized"] is False for row in rows)


def test_blocked_consumers_remain_legacy(built):
    registry = load(built / "remaining_legacy_blocker_registry.json")
    assert registry["remaining_legacy_consumer_count"] == 806
    assert registry["state"] == "UNCHANGED_REMAIN_LEGACY"
    assert registry["cutover_authorized"] is False


def test_handoff_boundary(built):
    handoff = load(built / "LCM13C_TO_LCM14A_HANDOFF.json")
    assert handoff["handoff_type"] == "LCM13C_TO_LCM14A"
    assert handoff["deprecation_candidate_count"] == 613
    assert handoff["remaining_legacy_consumer_count"] == 806
    assert handoff["reference_rehearsal_only"] is True
    assert handoff["live_state_mutation_performed"] is False
    for key in (
        "quarantine_authority_created",
        "deletion_authority_created",
        "runtime_authority_created",
        "live_order_authority_created",
        "capital_authority_created",
    ):
        assert handoff[key] is False


def test_acceptance_and_hostile_review_pass(built):
    acceptance = load(built / "reports/acceptance_report.json")
    hostile = load(built / "reports/hostile_review_report.json")
    assert acceptance["passed"] is True
    assert acceptance["reference_rehearsal_only"] is True
    assert acceptance["non_compensatory_gate_failures"] == []
    assert hostile["result"] == "PASS"
    assert len(hostile["attacks"]) >= 7
