from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):return lambda p:json.loads((root/p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def ex():return 'lab/11_strategy_factory/examples/saed_v4_19'
@pytest.fixture(scope='session')
def art():return 'lab/11_strategy_factory/artifacts/saed_v4_19'
