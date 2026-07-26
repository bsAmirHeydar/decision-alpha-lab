from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_10c.static_validation import validate_python
def test_python_static_valid():assert validate_python(Path('src/engine/tooling/strategy_factory/lcm/lcm_10c'))['result']=='PASS'
