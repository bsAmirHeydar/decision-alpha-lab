from src.engine.tooling.strategy_factory.lcm.lcm_05.schema_validation import validate as schemas
from src.engine.tooling.strategy_factory.lcm.lcm_05.static_validation import validate as static

def test_schemas(repo_root):
    r=schemas(repo_root);assert r['passed'];assert r['schema_count']==29
def test_policies_and_static(repo_root):
    r=static(repo_root);assert r['passed'];assert r['policy_count']==26;assert not r['forbidden_findings']
