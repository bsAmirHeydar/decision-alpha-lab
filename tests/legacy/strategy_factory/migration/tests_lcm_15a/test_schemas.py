from tools.strategy_factory.lcm.lcm_15a.schema_validation import validate_schemas
def test_schemas(repo_root): assert validate_schemas(repo_root/"registry/legacy_context_migration/lcm_15a/schemas/v1")>=13
