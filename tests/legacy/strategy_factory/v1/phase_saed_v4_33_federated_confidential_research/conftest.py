from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__);PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path:sys.path.insert(0,str(PY))
@pytest.fixture
def inputs():return json.loads((ROOT/"examples/legacy/strategy_factory/saed_v4_33/FULL_REFERENCE_INPUT.JSON").read_text())
@pytest.fixture
def result(inputs):
 from saed_v4_federated_confidential_research.service import run
 return run(inputs)
