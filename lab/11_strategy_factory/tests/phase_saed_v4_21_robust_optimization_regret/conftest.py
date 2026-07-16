from pathlib import Path
import json,sys,copy,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def config(root):return load(root/'lab/11_strategy_factory/examples/saed_v4_21/FULL_REFERENCE_CONFIG.JSON')
@pytest.fixture(scope='session')
def upstream(root):return load(root/'lab/11_strategy_factory/examples/saed_v4_21/UPSTREAM_V4_20_DOCUMENTS.JSON')
@pytest.fixture(scope='session')
def score(root):return load(root/'lab/11_strategy_factory/examples/saed_v4_21/GOLDEN_CANDIDATE_SCORE_TABLE.JSON')
@pytest.fixture(scope='session')
def result(config,upstream,score):
    from saed_v4_robust_optimization_regret.service import run_reference
    return run_reference(config,upstream,score)
