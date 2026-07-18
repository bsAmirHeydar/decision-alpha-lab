from tools.strategy_factory.lcm.lcm_01.static_validation import validate_registries
from tools.strategy_factory.lcm.lcm_01.delivery_validation import validate_delivery

def test_schemas_policies_and_registries(repo_root):
    r=validate_registries(repo_root); assert r['passed']; assert r['schema_count']>=15; assert r['machine_contract_count']>=25

def test_delivery_contract(repo_root):
    assert validate_delivery(repo_root)['passed']
