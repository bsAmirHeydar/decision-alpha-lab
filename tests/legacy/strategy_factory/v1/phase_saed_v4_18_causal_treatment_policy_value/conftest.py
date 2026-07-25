from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):return lambda p:json.loads((root/p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def art():return 'releases/history/strategy_factory/artifacts/saed_v4_18'
@pytest.fixture(scope='session')
def ex():return 'examples/legacy/strategy_factory/saed_v4_18'
