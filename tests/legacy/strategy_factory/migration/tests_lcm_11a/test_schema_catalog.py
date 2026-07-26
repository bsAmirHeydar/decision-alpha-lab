from src.engine.tooling.strategy_factory.lcm.lcm_11a.schema_validation import validate_schema_catalog
def test_schema_catalog(repo_root):
    result=validate_schema_catalog(repo_root/'registry/history/lcm/lcm_11a/schemas/v1')
    assert result['result']=='PASS'
    assert result['schema_count']==9
