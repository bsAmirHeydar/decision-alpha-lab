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
def records(load):return load('examples/legacy/strategy_factory/saed_v4_11/reference_corpus_records.json')
@pytest.fixture(scope='session')
def config(load):return load('examples/legacy/strategy_factory/saed_v4_11/reference_training_config.json')
@pytest.fixture(scope='session')
def upstream(load):return load('releases/history/strategy_factory/artifacts/saed_v4_10/GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON')
