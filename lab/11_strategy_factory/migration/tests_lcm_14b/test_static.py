from pathlib import Path
from tools.strategy_factory.lcm.lcm_14b.static_validation import static_validate
def test_static(): assert static_validate(Path(__file__).resolve().parents[4]/"tools/strategy_factory/lcm/lcm_14b")==[]
