def test_schemas_validate():
    from pathlib import Path
    from tools.strategy_factory.lcm.lcm_13a.schema_validation import validate_schema_directory
    root = Path("registry/legacy_context_migration/lcm_13a/schemas/v1")
    assert validate_schema_directory(root) == []
