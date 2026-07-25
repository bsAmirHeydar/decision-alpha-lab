import json
from datetime import datetime, timezone
from pathlib import Path

from strategy_factory.contracts import AnatomyEvent, Direction
from strategy_factory.optimization import compile_strategy_plan
from strategy_factory.plugins import PluginRegistry, register_builtins_from_spec
from strategy_factory.serving import CompiledCandidateFactory

SPEC = Path(__file__).resolve().parents[1] / "examples" / "manifests_v2" / "temporal_divergence_fast.json"


def test_compiled_candidate_factory_builds_bounded_candidates():
    spec = json.loads(SPEC.read_text())
    registry = PluginRegistry(); register_builtins_from_spec(spec, registry)
    plan = compile_strategy_plan(spec, registry)
    factory = CompiledCandidateFactory(plan)
    t = datetime(2026, 1, 1, tzinfo=timezone.utc)
    event = AnatomyEvent("e", plan.strategy_id, plan.strategy_version, "NQ", Direction.LONG, t, t, t, 100, 99)
    candidates = factory.build(event, {"confirmation_close": 100.2, "atr": 1.0})
    assert len(candidates) == 3
    assert candidates[0].target_price > candidates[0].entry_price
