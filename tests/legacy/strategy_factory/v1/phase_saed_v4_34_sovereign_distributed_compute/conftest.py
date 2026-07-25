from __future__ import annotations
from tools.repository_paths import find_repository_root
import copy,json,sys
from pathlib import Path
ROOT=find_repository_root(__file__); PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
import pytest
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def inputs(root): return json.loads((root/"examples/legacy/strategy_factory/saed_v4_34/GOLDEN_INPUT.JSON").read_text())
@pytest.fixture
def cloned(inputs): return copy.deepcopy(inputs)
