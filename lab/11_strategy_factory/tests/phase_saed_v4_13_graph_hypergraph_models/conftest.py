from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):return lambda p:json.loads((root/p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def inputs(load):return {'graph':load('lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),'receipt':load('lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_GRAPH_INTEGRITY_RECEIPT.json'),'handoff':load('lab/11_strategy_factory/artifacts/saed_v4_12/V4_12_TO_V4_13_HANDOFF.JSON'),'registry':load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON'),'distill':load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_DISTILLATION.JSON'),'snapshots':load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_STATE_SNAPSHOTS.JSON'),'spec':load('lab/11_strategy_factory/examples/saed_v4_13/reference_graph_spec.json'),'candidates':load('lab/11_strategy_factory/examples/saed_v4_13/reference_candidate_catalog.json'),'objectives':load('lab/11_strategy_factory/examples/saed_v4_13/reference_objective_catalog.json'),'envelope':load('lab/11_strategy_factory/examples/saed_v4_13/reference_compute_envelope.json')}
