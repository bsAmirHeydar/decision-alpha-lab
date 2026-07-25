from tools.repository_paths import find_repository_root
from pathlib import Path
from tools.strategy_factory.lcm.lcm_14b.static_validation import static_validate
def test_static(): assert static_validate(find_repository_root(__file__)/"src/engine/tooling/strategy_factory/lcm/lcm_14b")==[]
