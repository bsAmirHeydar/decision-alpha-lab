import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
import pytest
@pytest.fixture
def fixture():return json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_37/reference_input.json').read_text())
@pytest.fixture
def output():return json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_37/reference_output.json').read_text())
