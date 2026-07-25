import json

from tools.strategy_factory.lcm.lcm_14a.io import iter_jsonl
from tools.strategy_factory.lcm.lcm_14a.verify import verify_package


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_package_verifies(built):
    assert verify_package(built) == []


def test_exact_candidate_and_domain_counts(built):
    registry = load(built / "deprecation_registry.json")
    assert registry["candidate_count"] == 613
    assert registry["domain_counts"] == {"CONTEXT": 1, "DOCUMENTATION": 136, "TREATMENT": 422, "VISUAL": 54}


def test_redirect_modes_and_version_pins(built):
    registry = load(built / "compatibility_redirect_registry.json")
    rows = list(iter_jsonl(built / "records/compatibility_redirect_records.jsonl"))
    assert registry["redirect_count"] == len(rows) == 613
    assert registry["existing_redirect_active_count"] == 136
    assert registry["reference_only_redirect_count"] == 477
    assert registry["floating_version_count"] == 0
    assert all(row["canonical_version_pin"] == row["canonical_target_digest"] for row in rows)


def test_original_bytes_and_authority_boundary(built):
    rows = list(iter_jsonl(built / "records/deprecation_records.jsonl"))
    assert all(row["original_bytes_present"] is True for row in rows)
    assert all(row["quarantine_authorized"] is False for row in rows)
    assert all(row["deletion_authorized"] is False for row in rows)


def test_warning_catalog_is_actionable_and_early(built):
    catalog = load(built / "compatibility_warning_catalog.json")
    rows = list(iter_jsonl(built / "records/warning_records.jsonl"))
    assert catalog["warning_count"] == len(rows) == 613
    assert catalog["warning_before_resolution_count"] == 613
    assert catalog["behavior_change_count"] == 0
    assert all(row["legacy_locator"] in row["message"] and row["canonical_locator"] in row["message"] for row in rows)


def test_active_source_scope_is_blocked_from_quarantine(built):
    registry = load(built / "deprecation_registry.json")
    assert registry["active_source_blocked_count"] == 477
    rows = list(iter_jsonl(built / "records/deprecation_records.jsonl"))
    blocked = [row for row in rows if row["quarantine_readiness"] == "BLOCKED_DIRECT_ACTIVE_PATH"]
    assert len(blocked) == 477


def test_document_redirect_observation_candidates(built):
    registry = load(built / "quarantine_candidate_registry.json")
    rows = list(iter_jsonl(built / "records/quarantine_candidate_records.jsonl"))
    assert registry["observation_candidate_count"] == len(rows) == 136
    assert all(row["direct_runtime_use"] is False for row in rows)
    assert all(row["redirect_must_remain_active"] is True for row in rows)
    assert all(row["quarantine_move_authorized"] is False for row in rows)


def test_external_unknown_is_explicit_and_not_ignored(built):
    registry = load(built / "external_consumer_evidence_registry.json")
    rows = list(iter_jsonl(built / "records/external_consumer_evidence.jsonl"))
    assert registry["unknown_external_consumer_count"] == len(rows) == 613
    assert registry["ignored_unknown_count"] == 0
    assert all(row["evidence_state"] == "UNKNOWN" and row["ignored"] is False for row in rows)


def test_acceptance_hostile_and_handoff(built):
    acceptance = load(built / "reports/acceptance_report.json")
    hostile = load(built / "reports/hostile_review_report.json")
    handoff = load(built / "LCM14A_TO_LCM14B_HANDOFF.json")
    assert acceptance["passed"] is True
    assert acceptance["non_compensatory_gate_failures"] == []
    assert hostile["result"] == "PASS"
    assert len(hostile["attacks"]) >= 8
    assert handoff["handoff_type"] == "LCM14A_TO_LCM14B"
    assert handoff["observation_candidate_count"] == 136
    assert handoff["active_source_blocked_count"] == 477
