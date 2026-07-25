from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,json,copy
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
import pytest
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def config(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_22/FULL_REFERENCE_CONFIG.JSON').read_text())
@pytest.fixture(scope='session')
def upstream(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_22/UPSTREAM_V4_21_DOCUMENTS.JSON').read_text())
@pytest.fixture(scope='session')
def paths(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_22/REAL_REFERENCE_PATHS.JSON').read_text())
@pytest.fixture(scope='session')
def policy(root):return json.loads((root/'examples/legacy/strategy_factory/saed_v4_22/CANDIDATE_POLICY.JSON').read_text())
