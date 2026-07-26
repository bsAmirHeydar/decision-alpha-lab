from tools.repository_paths import find_repository_root
from pathlib import Path
from src.engine.tooling.strategy_factory.contexts.rthp.fixtures import validate_fixtures
ROOT=find_repository_root(__file__)/'contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1'
def test_all_golden_fixtures():
 r=validate_fixtures(ROOT);assert r["passed"],r
