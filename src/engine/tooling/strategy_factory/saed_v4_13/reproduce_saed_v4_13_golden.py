from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_graph_hypergraph_models.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text())
b=build_reference_bundle(load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_GRAPH_INTEGRITY_RECEIPT.json'),load('releases/history/strategy_factory/artifacts/saed_v4_12/V4_12_TO_V4_13_HANDOFF.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_DISTILLATION.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_STATE_SNAPSHOTS.JSON'),load('examples/legacy/strategy_factory/saed_v4_13/reference_graph_spec.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_objective_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_13/reference_compute_envelope.json'))
checks={'compiled_graph':load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),'tournament':load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),'checkpoint_registry':load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),'handoff':load('releases/history/strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON')}
for k,v in checks.items():assert b[k]==v,k
print('SAED V4-13 deterministic golden reproduction passed')
