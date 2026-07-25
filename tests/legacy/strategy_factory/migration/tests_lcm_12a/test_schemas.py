from tools.repository_paths import find_repository_root
from pathlib import Path
from tools.strategy_factory.lcm.lcm_12a.schema_validation import validate_schemas
ROOT=find_repository_root(__file__)
def test_schemas_are_valid():assert validate_schemas(ROOT/'registry/legacy_context_migration/lcm_12a/schemas/v1')==[]
