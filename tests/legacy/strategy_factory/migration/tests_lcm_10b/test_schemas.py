from tools.strategy_factory.lcm.lcm_10b.schema_validation import validate_schema_directory
from .conftest import SCHEMAS
def test_schema_catalog_is_valid():assert validate_schema_directory(SCHEMAS)["schema_count"]>=16
