from pathlib import Path
import json,sys,pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
@pytest.fixture(scope='session')
def root():return ROOT
@pytest.fixture(scope='session')
def load(root):
    def f(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
    return f
@pytest.fixture(scope='session')
def upstream(load):
    return (load('lab/11_strategy_factory/artifacts/saed_v4_04/GOLDEN_MULTIMODAL_VIEW_PACKAGE.json'),load('lab/11_strategy_factory/artifacts/saed_v4_05/GOLDEN_SEMANTIC_TEMPORAL_HYPERGRAPH.json'),load('lab/11_strategy_factory/artifacts/saed_v4_07/GOLDEN_ACTION_LATTICE.JSON'),load('lab/11_strategy_factory/artifacts/saed_v4_09/GOLDEN_EXECUTION_TWIN.JSON'))
