import json,sys
from copy import deepcopy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture
def fixture():return json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_40/reference_fixture.json').read_text())
@pytest.fixture(scope="session")
def reference_output():return json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_40/reference_output.json').read_text())
