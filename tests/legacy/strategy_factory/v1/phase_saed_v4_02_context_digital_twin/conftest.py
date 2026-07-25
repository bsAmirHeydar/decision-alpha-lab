from tools.repository_paths import find_repository_root
import sys,json
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture
def root():return ROOT
@pytest.fixture
def context_spec(ROOT=None):
    r=find_repository_root(__file__);return json.loads((r/'examples/legacy/strategy_factory/saed_v4_02/golden_context_specification.json').read_text())
@pytest.fixture
def seed():
    r=find_repository_root(__file__);return json.loads((r/'examples/legacy/strategy_factory/saed_v4_02/golden_twin_seed.json').read_text())
