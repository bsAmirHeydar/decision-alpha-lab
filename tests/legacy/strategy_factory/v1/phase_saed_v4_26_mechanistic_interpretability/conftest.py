from __future__ import annotations
from tools.repository_paths import find_repository_root
import json, sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
PYTHON_ROOT=ROOT/"src/engine/packages"
if str(PYTHON_ROOT) not in sys.path: sys.path.insert(0,str(PYTHON_ROOT))
EXAMPLES=ROOT/"examples/legacy/strategy_factory/saed_v4_26"; ARTIFACTS=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_26"; SCHEMAS=ROOT/"schemas/legacy/strategy_factory/saed_v4_26"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
@pytest.fixture(scope="session")
def config(): return load(EXAMPLES/"FULL_REFERENCE_CONFIG.JSON")
@pytest.fixture(scope="session")
def upstream(): return load(EXAMPLES/"UPSTREAM_V4_25_DOCUMENTS.JSON")
@pytest.fixture(scope="session")
def records(): return load(EXAMPLES/"MODEL_MECHANISM_RECORDS.JSON")
@pytest.fixture(scope="session")
def golden(): return {p.name:load(p) for p in ARTIFACTS.glob("*.JSON")}

@pytest.fixture(scope="session")
def outputs(config,upstream,records):
    from saed_v4_mechanistic_interpretability import run
    return run(config,upstream,records)
