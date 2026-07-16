from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_20'
ART=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_20'
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
