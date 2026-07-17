from __future__ import annotations
import json, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
PYTHON_ROOT=ROOT/"lab/11_strategy_factory/python"
if str(PYTHON_ROOT) not in sys.path: sys.path.insert(0,str(PYTHON_ROOT))
EXAMPLES=ROOT/"lab/11_strategy_factory/examples/saed_v4_26"; ARTIFACTS=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_26"; SCHEMAS=ROOT/"lab/11_strategy_factory/schemas/saed_v4_26"
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
