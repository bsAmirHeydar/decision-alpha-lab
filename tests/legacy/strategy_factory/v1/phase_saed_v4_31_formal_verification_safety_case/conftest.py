from tools.repository_paths import find_repository_root
import copy,json,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
PY_ROOT=ROOT/"src/engine/packages"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_31"
def load(name): return json.loads((EX/name).read_text(encoding="utf-8"))
@pytest.fixture(scope="session")
def inputs(): return load("FULL_REFERENCE_INPUT.JSON")
@pytest.fixture(scope="session")
def result(inputs):
 from saed_v4_formal_verification_safety_case.service import run
 return run(inputs)
@pytest.fixture
def clone(inputs): return copy.deepcopy(inputs)
