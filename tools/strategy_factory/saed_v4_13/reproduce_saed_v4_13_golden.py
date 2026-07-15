from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_graph_hypergraph_models.service import build_reference_bundle
load=lambda p:json.loads((ROOT/p).read_text())
b=build_reference_bundle(load('lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),load('lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_GRAPH_INTEGRITY_RECEIPT.json'),load('lab/11_strategy_factory/artifacts/saed_v4_12/V4_12_TO_V4_13_HANDOFF.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_DISTILLATION.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_STATE_SNAPSHOTS.JSON'),load('lab/11_strategy_factory/examples/saed_v4_13/reference_graph_spec.json'),load('lab/11_strategy_factory/examples/saed_v4_13/reference_candidate_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_13/reference_objective_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_13/reference_compute_envelope.json'))
checks={'compiled_graph':load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),'tournament':load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),'checkpoint_registry':load('lab/11_strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),'handoff':load('lab/11_strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON')}
for k,v in checks.items():assert b[k]==v,k
print('SAED V4-13 deterministic golden reproduction passed')
