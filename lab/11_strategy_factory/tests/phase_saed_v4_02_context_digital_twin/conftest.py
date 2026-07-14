import sys,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture
def root():return ROOT
@pytest.fixture
def context_spec(ROOT=None):
    r=Path(__file__).resolve().parents[4];return json.loads((r/'lab/11_strategy_factory/examples/saed_v4_02/golden_context_specification.json').read_text())
@pytest.fixture
def seed():
    r=Path(__file__).resolve().parents[4];return json.loads((r/'lab/11_strategy_factory/examples/saed_v4_02/golden_twin_seed.json').read_text())
