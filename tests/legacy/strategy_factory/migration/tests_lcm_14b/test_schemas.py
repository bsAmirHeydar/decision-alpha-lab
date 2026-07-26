from tools.repository_paths import find_repository_root
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_14b.schema_validation import validate_schema_directory
def test_schemas(): assert validate_schema_directory(find_repository_root(__file__)/"registry/history/lcm/lcm_14b/schemas/v1")==[]
