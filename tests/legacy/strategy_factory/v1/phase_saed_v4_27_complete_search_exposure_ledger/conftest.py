from __future__ import annotations
from tools.repository_paths import find_repository_root
import copy, json, sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
PYTHON_ROOT=ROOT/"src/engine/packages"
if str(PYTHON_ROOT) not in sys.path: sys.path.insert(0,str(PYTHON_ROOT))
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_27"; AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_27"; SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_27"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
@pytest.fixture(scope="session")
def config(): return load(EX/"FULL_REFERENCE_CONFIG.JSON")
@pytest.fixture(scope="session")
def upstream(): return load(EX/"UPSTREAM_V4_26_DOCUMENTS.JSON")
@pytest.fixture(scope="session")
def manifests(): return load(EX/"EXPERIMENT_MANIFESTS.JSON")
@pytest.fixture(scope="session")
def trials(): return load(EX/"TRIAL_EVENTS.JSON")
@pytest.fixture(scope="session")
def exposures(): return load(EX/"EXPOSURE_EVENTS.JSON")
@pytest.fixture(scope="session")
def outputs(config,upstream,manifests,trials,exposures):
    from saed_v4_complete_search_exposure_ledger import run
    return run(config,upstream,manifests,trials,exposures)
