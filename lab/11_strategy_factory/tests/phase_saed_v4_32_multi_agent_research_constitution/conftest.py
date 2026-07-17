from __future__ import annotations
import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
@pytest.fixture
def inputs(): return json.loads((ROOT/"lab/11_strategy_factory/examples/saed_v4_32/FULL_REFERENCE_INPUT.JSON").read_text())
@pytest.fixture
def result(inputs):
 from saed_v4_multi_agent_research_constitution.service import run
 return run(inputs)
