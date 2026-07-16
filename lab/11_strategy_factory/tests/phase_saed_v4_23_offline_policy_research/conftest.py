from pathlib import Path
import sys,json,copy,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_23';ART=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_23';SCH=ROOT/'lab/11_strategy_factory/schemas/saed_v4_23'
def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def config():return load(EX/'FULL_REFERENCE_CONFIG.JSON')
@pytest.fixture(scope='session')
def upstream():return load(EX/'UPSTREAM_V4_22_DOCUMENTS.JSON')
@pytest.fixture(scope='session')
def dataset():return load(EX/'LOGGED_TRAJECTORIES.JSON')
@pytest.fixture(scope='session')
def baseline():return load(EX/'MANUAL_BASELINE_POLICY.JSON')
