from tools.repository_paths import find_repository_root
import json,sys
from copy import deepcopy
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture
def fixture():return json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_40/reference_fixture.json').read_text())
@pytest.fixture(scope="session")
def reference_output():return json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_40/reference_output.json').read_text())
