from tools.repository_paths import find_repository_root
import copy,json,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_prospective_shadow_micro_live import run_reference
@pytest.fixture(scope="session")
def fixture_data():return json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_39/reference_input.json').read_text())
@pytest.fixture
def fixture(fixture_data):return copy.deepcopy(fixture_data)
@pytest.fixture(scope="session")
def output(fixture_data):return run_reference(copy.deepcopy(fixture_data))
