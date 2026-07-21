from pathlib import Path
from tools.strategy_factory.contexts.rthp.fixtures import validate_fixtures
ROOT=Path(__file__).resolve().parents[4]/'lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1'
def test_all_golden_fixtures():
 r=validate_fixtures(ROOT);assert r["passed"],r
