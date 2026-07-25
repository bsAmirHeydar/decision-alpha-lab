from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys,pytest
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):
    def f(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
    return f
@pytest.fixture(scope='session')
def upstream(load):
    return (load('releases/history/strategy_factory/artifacts/saed_v4_04/GOLDEN_MULTIMODAL_VIEW_PACKAGE.json'),load('releases/history/strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),load('releases/history/strategy_factory/artifacts/saed_v4_07/GOLDEN_ACTION_LATTICE.JSON'),load('releases/history/strategy_factory/artifacts/saed_v4_09/GOLDEN_EXECUTION_TWIN.JSON'))
