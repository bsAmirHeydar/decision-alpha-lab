from src.engine.tooling.strategy_factory.lcm.lcm_15c.schema_validation import validate_schemas
def test_schemas(repo_root):assert validate_schemas(repo_root/'registry/history/lcm/lcm_15c/schemas/v1')>=13
