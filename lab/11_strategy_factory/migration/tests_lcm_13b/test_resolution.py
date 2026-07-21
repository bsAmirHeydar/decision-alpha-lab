from __future__ import annotations
from tools.strategy_factory.lcm.lcm_13b.io import iter_jsonl
from tools.strategy_factory.lcm.lcm_13b.resolver import ConsumerLocatorResolver

def test_all_cutover_consumers_resolve_canonical(cutover_root):
    bindings_path = cutover_root / "records/active_consumer_bindings.jsonl"
    resolver = ConsumerLocatorResolver(bindings_path)
    for row in iter_jsonl(bindings_path):
        resolved = resolver.resolve(row["consumer_id"])
        assert resolved.resolved_locator == row["active_locator"]
        assert resolved.fallback_locator == row["prior_locator"]
        assert resolved.primary_mode == "CANONICAL_PRIMARY_LEGACY_FALLBACK"
        assert resolved.cutover_state == "REFERENCE_CANONICAL_ACTIVE"

def test_blocked_consumers_stay_legacy(cutover_root):
    for row in iter_jsonl(cutover_root / "records/remaining_legacy_consumers.jsonl"):
        assert row["cutover_state"] == "BLOCKED_REMAIN_LEGACY"
        assert row["wave_id"] is None
        assert row["active_locator"]
