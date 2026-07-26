from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_10c.schema_validation import validate_schema_catalog
def test_schema_catalog_valid():assert validate_schema_catalog(Path('registry/history/lcm/lcm_10c/schemas/v1'))['result']=='PASS'
