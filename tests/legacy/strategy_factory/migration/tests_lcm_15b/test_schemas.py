from src.engine.tooling.strategy_factory.lcm.lcm_15b.schema_validation import validate_schemas
def test_schemas(repo_root):assert validate_schemas(repo_root/"registry/history/lcm/lcm_15b/schemas/v1")>=12
