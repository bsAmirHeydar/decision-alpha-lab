from tools.strategy_factory.lcm.lcm_12b.schema_validation import validate_schema_directory
def test_schemas(repo_root):
    assert validate_schema_directory(repo_root/"registry/legacy_context_migration/lcm_12b/schemas/v1")==[]
