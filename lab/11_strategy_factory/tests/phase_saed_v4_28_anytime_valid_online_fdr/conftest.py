from __future__ import annotations
import copy,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]; PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_28"; AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_28"; SC=ROOT/"lab/11_strategy_factory/schemas/saed_v4_28"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
@pytest.fixture(scope="session")
def config(): return load(EX/"FULL_REFERENCE_CONFIG.JSON")
@pytest.fixture(scope="session")
def upstream(): return load(EX/"UPSTREAM_V4_27_DOCUMENTS.JSON")
@pytest.fixture(scope="session")
def hypotheses(): return load(EX/"HYPOTHESIS_STREAM.JSON")
@pytest.fixture(scope="session")
def outputs(config,upstream,hypotheses):
    from saed_v4_anytime_valid_online_fdr import run
    return run(config,upstream,hypotheses)
