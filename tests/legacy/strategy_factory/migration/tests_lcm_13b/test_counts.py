from __future__ import annotations
from src.engine.tooling.strategy_factory.lcm.lcm_13b.io import iter_jsonl, load_json

def test_exact_consumer_accounting(cutover_root):
    bindings = list(iter_jsonl(cutover_root / "records/active_consumer_bindings.jsonl"))
    blocked = list(iter_jsonl(cutover_root / "records/remaining_legacy_consumers.jsonl"))
    assert len(bindings) == 613
    assert len(blocked) == 806
    assert len(bindings) + len(blocked) == 1419
    assert not ({r["consumer_id"] for r in bindings} & {r["consumer_id"] for r in blocked})

def test_domain_counts(cutover_root):
    from collections import Counter
    bindings = list(iter_jsonl(cutover_root / "records/active_consumer_bindings.jsonl"))
    assert Counter(r["domain"] for r in bindings) == {"CONTEXT": 1, "DOCUMENTATION": 136, "TREATMENT": 422, "VISUAL": 54}
    acceptance = load_json(cutover_root / "reports/acceptance_report.json")
    assert acceptance["cutover_consumer_count"] == 613
    assert acceptance["blocked_consumer_count"] == 806
