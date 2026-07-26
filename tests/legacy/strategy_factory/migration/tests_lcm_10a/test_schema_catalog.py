from src.engine.tooling.strategy_factory.lcm.lcm_10a.schema_validation import validate_schema_directory
from .conftest import SCHEMAS
def test_all_schemas_are_valid_2020_12():assert validate_schema_directory(SCHEMAS)['schema_count']>=15
