from pathlib import Path
from tools.strategy_factory.lcm.lcm_12a.static_validation import validate_module
ROOT=Path(__file__).resolve().parents[4]
def test_module_has_no_runtime_or_order_authority():assert validate_module(ROOT/'tools/strategy_factory/lcm/lcm_12a')==[]
