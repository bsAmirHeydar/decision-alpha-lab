from pathlib import Path
from tools.strategy_factory.lcm.lcm_10c.schema_validation import validate_schema_catalog
def test_schema_catalog_valid():assert validate_schema_catalog(Path('registry/legacy_context_migration/lcm_10c/schemas/v1'))['result']=='PASS'
