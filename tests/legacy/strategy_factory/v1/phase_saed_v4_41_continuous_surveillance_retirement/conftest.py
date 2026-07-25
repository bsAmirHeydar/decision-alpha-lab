from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def fixture(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_41/reference_input.json').read_text())
@pytest.fixture(scope='session')
def output(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_41/reference_output.json').read_text())
