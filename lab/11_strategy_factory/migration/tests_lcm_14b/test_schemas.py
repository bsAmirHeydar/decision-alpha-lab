from pathlib import Path
from tools.strategy_factory.lcm.lcm_14b.schema_validation import validate_schema_directory
def test_schemas(): assert validate_schema_directory(Path(__file__).resolve().parents[4]/"registry/legacy_context_migration/lcm_14b/schemas/v1")==[]
