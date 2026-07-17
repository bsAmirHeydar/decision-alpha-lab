from __future__ import annotations
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
import pytest
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def inputs(root): return json.loads((root/"lab/11_strategy_factory/examples/saed_v4_34/GOLDEN_INPUT.JSON").read_text())
@pytest.fixture
def cloned(inputs): return copy.deepcopy(inputs)
