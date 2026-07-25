from tools.strategy_factory.lcm.lcm_15b.schema_validation import validate_schemas
def test_schemas(repo_root):assert validate_schemas(repo_root/"registry/legacy_context_migration/lcm_15b/schemas/v1")>=12
