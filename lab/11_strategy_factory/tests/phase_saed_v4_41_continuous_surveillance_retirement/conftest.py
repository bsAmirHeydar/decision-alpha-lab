import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def fixture(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_41/reference_input.json').read_text())
@pytest.fixture(scope='session')
def output(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_41/reference_output.json').read_text())
