import json
from pathlib import Path

from strategy_factory.optimization import compile_strategy_plan
from strategy_factory.plugins import PluginRegistry, register_builtins_from_spec


SPEC = Path(__file__).resolve().parents[1] / "examples" / "manifests_v2" / "temporal_divergence_fast.json"


def test_plan_compiles_and_preexpands_templates():
    spec = json.loads(SPEC.read_text())
    registry = PluginRegistry()
    register_builtins_from_spec(spec, registry)
    plan = compile_strategy_plan(spec, registry)
    assert plan.strategy_id == "exp0017_temporal_divergence_fast"
    assert len(plan.candidate_templates) == 3
    assert plan.describe()["feature_provider_order"] == ["market_state_core"]
    assert plan.plan_hash.startswith("plan_")
