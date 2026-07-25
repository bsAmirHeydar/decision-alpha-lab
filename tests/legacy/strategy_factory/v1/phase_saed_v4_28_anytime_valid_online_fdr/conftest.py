from __future__ import annotations
from tools.repository_paths import find_repository_root
import copy,json,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__); PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_28"; AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_28"; SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_28"
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
