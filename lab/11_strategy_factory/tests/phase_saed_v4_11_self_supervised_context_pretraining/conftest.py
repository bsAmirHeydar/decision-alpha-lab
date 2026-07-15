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
def records(load):return load('lab/11_strategy_factory/examples/saed_v4_11/reference_corpus_records.json')
@pytest.fixture(scope='session')
def config(load):return load('lab/11_strategy_factory/examples/saed_v4_11/reference_training_config.json')
@pytest.fixture(scope='session')
def upstream(load):return load('lab/11_strategy_factory/artifacts/saed_v4_10/GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON')
