from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
import pytest
@pytest.fixture
def fixture():return json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_37/reference_input.json').read_text())
@pytest.fixture
def output():return json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_37/reference_output.json').read_text())
