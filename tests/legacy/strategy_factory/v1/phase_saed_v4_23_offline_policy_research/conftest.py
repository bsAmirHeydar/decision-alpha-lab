from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,json,copy,pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_23';ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_23';SCH=ROOT/'schemas/legacy/strategy_factory/saed_v4_23'
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def config():return load(EX/'FULL_REFERENCE_CONFIG.JSON')
@pytest.fixture(scope='session')
def upstream():return load(EX/'UPSTREAM_V4_22_DOCUMENTS.JSON')
@pytest.fixture(scope='session')
def dataset():return load(EX/'LOGGED_TRAJECTORIES.JSON')
@pytest.fixture(scope='session')
def baseline():return load(EX/'MANUAL_BASELINE_POLICY.JSON')
