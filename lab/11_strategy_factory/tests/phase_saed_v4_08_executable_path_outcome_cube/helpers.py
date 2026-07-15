from pathlib import Path
import json
from saed_v4_outcome_cube import ContextSnapshot,PriceObservation,OutcomePolicy,CostRegistry,build_cube
ROOT=Path(__file__).resolve().parents[4]
def load(rel):return json.loads((ROOT/rel).read_text())
def inputs(path='lab/11_strategy_factory/examples/saed_v4_08/golden_market_path.json'):
 lattice=load('lab/11_strategy_factory/artifacts/saed_v4_07/GOLDEN_ACTION_LATTICE.JSON');handoff=load('lab/11_strategy_factory/artifacts/saed_v4_07/V4_07_TO_V4_08_HANDOFF.JSON');context=ContextSnapshot.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_08/golden_context_snapshot.json'));obs=[PriceObservation.from_mapping(x) for x in load(path)['observations']];policy=OutcomePolicy.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_08/outcome_policy.json'));reg=CostRegistry.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_08/cost_registry.json'));return lattice,handoff,context,obs,policy,reg
def cube():return build_cube(*inputs(),'fixed_conservative','1.0.0')
