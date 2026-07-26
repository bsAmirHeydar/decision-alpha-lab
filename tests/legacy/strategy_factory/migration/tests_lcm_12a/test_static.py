from tools.repository_paths import find_repository_root
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_12a.static_validation import validate_module
ROOT=find_repository_root(__file__)
def test_module_has_no_runtime_or_order_authority():assert validate_module(ROOT/'src/engine/tooling/strategy_factory/lcm/lcm_12a')==[]
