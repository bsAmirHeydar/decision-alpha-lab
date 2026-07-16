from pathlib import Path
import sys,json,copy
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
import pytest
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def config(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_22/FULL_REFERENCE_CONFIG.JSON').read_text())
@pytest.fixture(scope='session')
def upstream(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_22/UPSTREAM_V4_21_DOCUMENTS.JSON').read_text())
@pytest.fixture(scope='session')
def paths(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_22/REAL_REFERENCE_PATHS.JSON').read_text())
@pytest.fixture(scope='session')
def policy(root):return json.loads((root/'lab/11_strategy_factory/examples/saed_v4_22/CANDIDATE_POLICY.JSON').read_text())
