from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);PY=ROOT/'src/engine/packages';sys.path.insert(0,str(PY))
from saed_v4_outcome_cube import ContextSnapshot,PriceObservation,OutcomePolicy,CostRegistry,build_cube,summarize,build_receipt,build_v4_09_handoff
from saed_v4_outcome_cube.serialization import cube_to_dict
from saed_v4_outcome_cube.partition import partition_nodes
from saed_v4_outcome_cube.telemetry import telemetry
load=lambda p:json.loads((ROOT/p).read_text())
lattice=load('releases/history/strategy_factory/artifacts/saed_v4_07/GOLDEN_ACTION_LATTICE.JSON');handoff=load('releases/history/strategy_factory/artifacts/saed_v4_07/V4_07_TO_V4_08_HANDOFF.JSON');ctx=ContextSnapshot.from_mapping(load('examples/legacy/strategy_factory/saed_v4_08/golden_context_snapshot.json'));obs=[PriceObservation.from_mapping(x) for x in load('examples/legacy/strategy_factory/saed_v4_08/golden_market_path.json')['observations']];pol=OutcomePolicy.from_mapping(load('examples/legacy/strategy_factory/saed_v4_08/outcome_policy.json'));reg=CostRegistry.from_mapping(load('examples/legacy/strategy_factory/saed_v4_08/cost_registry.json'));cube=build_cube(lattice,handoff,ctx,obs,pol,reg,'fixed_conservative','1.0.0')
out=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_08';out.mkdir(parents=True,exist_ok=True)
for name,obj in [('GOLDEN_OUTCOME_CUBE.JSON',cube_to_dict(cube)),('GOLDEN_CUBE_SUMMARY.JSON',summarize(cube)),('GOLDEN_INTEGRITY_RECEIPT.JSON',build_receipt(cube)),('GOLDEN_PARTITION_MANIFEST.JSON',partition_nodes(lattice,4)),('GOLDEN_TELEMETRY.JSON',telemetry(cube)),('V4_08_TO_V4_09_HANDOFF.JSON',build_v4_09_handoff(cube))]:(out/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(cube.cube_hash)
