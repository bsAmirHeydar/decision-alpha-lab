import json
from src.engine.tooling.strategy_factory.lcm.lcm_16a.canonical import object_digest


def test_rthp_protected_engine_amendment_is_exact(root):
    path = root / "contexts/legacy/strategy_factory/generated/rthp_cross_symbol_cycle_divergence/ai_input/generated/engine_extended_baseline_amendment_lcm16a.json"
    amendment = json.loads(path.read_text())
    assert amendment["amendment_count"] == 6
    assert amendment["amendment_digest"] == object_digest(amendment, "amendment_digest")
    assert not amendment["runtime_authority_created"]
    assert not amendment["order_authority_created"]
    assert not amendment["capital_authority_created"]
