def test_schemas_validate():
    from pathlib import Path
    from src.engine.tooling.strategy_factory.lcm.lcm_13a.schema_validation import validate_schema_directory
    root = Path("registry/history/lcm/lcm_13a/schemas/v1")
    assert validate_schema_directory(root) == []
