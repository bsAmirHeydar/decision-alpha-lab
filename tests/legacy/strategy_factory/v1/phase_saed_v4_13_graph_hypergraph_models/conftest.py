from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):return lambda p:json.loads((root/p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def inputs(load):return {'graph':load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),'receipt':load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_GRAPH_INTEGRITY_RECEIPT.json'),'handoff':load('releases/history/strategy_factory/artifacts/saed_v4_12/V4_12_TO_V4_13_HANDOFF.JSON'),'registry':load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_CHECKPOINT_REGISTRY.JSON'),'distill':load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_DISTILLATION.JSON'),'snapshots':load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_STATE_SNAPSHOTS.JSON'),'spec':load('examples/legacy/strategy_factory/saed_v4_13/reference_graph_spec.json'),'candidates':load('examples/legacy/strategy_factory/saed_v4_13/reference_candidate_catalog.json'),'objectives':load('examples/legacy/strategy_factory/saed_v4_13/reference_objective_catalog.json'),'envelope':load('examples/legacy/strategy_factory/saed_v4_13/reference_compute_envelope.json')}
