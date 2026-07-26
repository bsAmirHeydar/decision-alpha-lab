from __future__ import annotations
from src.engine.tooling.strategy_factory.lcm.lcm_13b.constants import EVENT_TYPES, WAVE_SIZE_LIMITS
from src.engine.tooling.strategy_factory.lcm.lcm_13b.io import iter_jsonl, load_json

def test_wave_limits_and_exact_coverage(cutover_root):
    registry = load_json(cutover_root / "consumer_wave_registry.json")
    bindings = list(iter_jsonl(cutover_root / "records/active_consumer_bindings.jsonl"))
    seen = []
    for wave in registry["waves"]:
        plan = load_json(cutover_root / "consumer_wave_plans" / f"{wave['wave_id']}.json")
        assert plan["consumer_count"] <= WAVE_SIZE_LIMITS[plan["domain"]]
        assert plan["consumer_count"] == len(plan["consumer_ids"])
        assert plan["partial_wave_allowed"] is False
        seen.extend(plan["consumer_ids"])
    assert sorted(seen) == sorted(r["consumer_id"] for r in bindings)
    assert len(seen) == len(set(seen))

def test_wave_artifacts_are_consistent(cutover_root):
    registry = load_json(cutover_root / "consumer_wave_registry.json")
    for wave in registry["waves"]:
        wave_id = wave["wave_id"]
        plan = load_json(cutover_root / "consumer_wave_plans" / f"{wave_id}.json")
        manifest = load_json(cutover_root / "consumer_cutover_manifests" / f"{wave_id}.json")
        health = load_json(cutover_root / "post_cutover_health_reports" / f"{wave_id}.json")
        receipt = load_json(cutover_root / "locator_switch_receipts" / f"{wave_id}.json")
        rollback = load_json(cutover_root / "rollback_packages" / f"{wave_id}.json")
        assert plan["consumer_ids"] == manifest["consumer_ids"] == receipt["consumer_ids"]
        assert health["observation_status"] == "PASS"
        assert receipt["receipt_status"] == "PASS"
        assert rollback["preverified"] is True
        assert manifest["rollback_package_digest"] == rollback["rollback_package_digest"]

def test_event_ledger_sequence(cutover_root):
    registry = load_json(cutover_root / "consumer_wave_registry.json")
    events = list(iter_jsonl(cutover_root / "cutover_event_ledger.jsonl"))
    assert len(events) == registry["wave_count"] * len(EVENT_TYPES)
    assert [r["event_sequence"] for r in events] == list(range(1, len(events) + 1))
    for offset in range(0, len(events), len(EVENT_TYPES)):
        assert [r["event_type"] for r in events[offset:offset + len(EVENT_TYPES)]] == list(EVENT_TYPES)
