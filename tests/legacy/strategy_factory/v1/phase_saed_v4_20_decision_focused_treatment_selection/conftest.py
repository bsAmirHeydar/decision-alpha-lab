from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_20'
ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_20'
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))

@pytest.fixture
def config():
    return load(EX/'FULL_REFERENCE_CONFIG.JSON')

@pytest.fixture
def context():
    return load(EX/'GOLDEN_CONTEXT.JSON')

@pytest.fixture
def outcomes():
    return load(EX/'GOLDEN_OUTCOMES.JSON')

@pytest.fixture
def proofs():
    return load(EX/'GOLDEN_PROOFS.JSON')

@pytest.fixture
def upstream_hashes():
    return load(EX/'UPSTREAM_HASHES.JSON')

@pytest.fixture
def golden_result(config,context,outcomes,proofs,upstream_hashes):
    from saed_v4_decision_focused_treatment_selection.service import select_treatments
    return select_treatments(config,context,outcomes,proofs,upstream_hashes)
