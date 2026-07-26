from tools.repository_paths import find_repository_root
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_12a.schema_validation import validate_schemas
ROOT=find_repository_root(__file__)
def test_schemas_are_valid():assert validate_schemas(ROOT/'registry/history/lcm/lcm_12a/schemas/v1')==[]
