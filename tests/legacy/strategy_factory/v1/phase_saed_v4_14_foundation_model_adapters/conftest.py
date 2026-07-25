from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):return lambda p:json.loads((root/p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def inputs(load):
 return dict(v413_handoff=load('releases/history/strategy_factory/artifacts/saed_v4_13/V4_13_TO_V4_14_HANDOFF.JSON'),v413_registry=load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_CHECKPOINT_REGISTRY.JSON'),v413_embeddings=load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_CANDIDATE_EMBEDDINGS.JSON'),v413_graph=load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_COMPILED_MODEL_GRAPH.JSON'),v413_tournament=load('releases/history/strategy_factory/artifacts/saed_v4_13/GOLDEN_TOURNAMENT.JSON'),adapter_config_doc=load('examples/legacy/strategy_factory/saed_v4_14/reference_adapter_config.json'),intake_docs=load('examples/legacy/strategy_factory/saed_v4_14/reference_model_intake_catalog.json'),candidate_docs=load('examples/legacy/strategy_factory/saed_v4_14/reference_candidate_catalog.json'),disclosure_docs=load('examples/legacy/strategy_factory/saed_v4_14/reference_pretraining_disclosures.json'),domain_policy_doc=load('examples/legacy/strategy_factory/saed_v4_14/reference_domain_shift_policy.json'),budget_doc=load('examples/legacy/strategy_factory/saed_v4_14/reference_compute_exposure_budget.json'))
@pytest.fixture(scope='session')
def bundle(inputs):
 from saed_v4_foundation_model_adapters.service import build_reference_bundle
 return build_reference_bundle(**inputs)
