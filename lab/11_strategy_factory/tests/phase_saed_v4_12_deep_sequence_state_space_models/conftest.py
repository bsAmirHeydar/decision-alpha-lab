from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):
 def f(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
 return f
@pytest.fixture(scope='session')
def upstream(load):return (load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKENIZER_SPEC.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_CHECKPOINT_REGISTRY.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'))
@pytest.fixture(scope='session')
def config(load):return load('lab/11_strategy_factory/examples/saed_v4_12/reference_sequence_spec.json'),load('lab/11_strategy_factory/examples/saed_v4_12/reference_candidate_catalog.json'),load('lab/11_strategy_factory/examples/saed_v4_12/reference_reset_policy.json')
@pytest.fixture(scope='session')
def golden(load):return load('lab/11_strategy_factory/artifacts/saed_v4_12/GOLDEN_TOURNAMENT.JSON')
