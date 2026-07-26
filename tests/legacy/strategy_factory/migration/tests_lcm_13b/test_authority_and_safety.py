from __future__ import annotations
from src.engine.tooling.strategy_factory.lcm.lcm_13b.io import iter_jsonl, load_json

def test_no_runtime_order_or_capital_authority(cutover_root):
    for path in [
        "records/active_consumer_bindings.jsonl",
        "records/remaining_legacy_consumers.jsonl",
    ]:
        for row in iter_jsonl(cutover_root / path):
            assert row["runtime_authority"] is False
            assert row["live_order_authority"] is False
            assert row["capital_authority"] is False
    handoff = load_json(cutover_root / "LCM13B_TO_LCM13C_HANDOFF.json")
    assert handoff["runtime_authority_created"] is False
    assert handoff["live_order_authority_created"] is False
    assert handoff["capital_authority_created"] is False

def test_no_source_deletion_or_default_change(cutover_root):
    acceptance = load_json(cutover_root / "reports/acceptance_report.json")
    assert acceptance["source_file_change_count"] == 0
    assert acceptance["configuration_default_change_count"] == 0
    assert acceptance["legacy_source_delete_count"] == 0

def test_compatibility_adapters_are_transition_only(cutover_root):
    rows = list(iter_jsonl(cutover_root / "records/compatibility_adapter_records.jsonl"))
    assert len(rows) == 613
    assert all(row["permanent_architecture"] is False for row in rows)
    assert all(row["removal_candidate_after"] == "LCM13C_VERIFIED_ROLLBACK_AND_FORWARD_RECOVERY" for row in rows)

def test_post_cutover_mismatch_registry_is_raw_and_empty(cutover_root):
    registry = load_json(cutover_root / "post_cutover_mismatch_registry.json")
    assert registry["post_cutover_mismatch_count"] == 0
    assert registry["post_cutover_high_critical_mismatch_count"] == 0
    assert registry["suppressed_mismatch_count"] == 0
    assert registry["aggregation_rule_count"] == 0
    assert list(iter_jsonl(cutover_root / registry["records_path"])) == []
