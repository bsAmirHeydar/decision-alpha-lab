from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):
 def f(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
 return f
@pytest.fixture(scope='session')
def upstream(load):return (load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'))
@pytest.fixture(scope='session')
def config(load):return load('examples/legacy/strategy_factory/saed_v4_12/reference_sequence_spec.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_candidate_catalog.json'),load('examples/legacy/strategy_factory/saed_v4_12/reference_reset_policy.json')
@pytest.fixture(scope='session')
def golden(load):return load('releases/history/strategy_factory/artifacts/saed_v4_12/GOLDEN_TOURNAMENT.JSON')
