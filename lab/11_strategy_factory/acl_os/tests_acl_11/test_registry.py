from tools.strategy_factory.acl_os.acl_11.static_validation import validate_registry
def test_static_registry(root):
    r=validate_registry(root); assert r['passed']; assert r['schema_count']>=20 and r['policy_count']>=20
def test_no_forbidden_mql5_api(root): assert validate_registry(root)['forbidden_mql5_hits']==[]
