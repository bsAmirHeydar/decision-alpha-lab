from tools.strategy_factory.acl_os.acl_13.static_validation import validate_registry
from tools.strategy_factory.acl_os.acl_13.delivery_validation import validate_delivery
def test_registry_valid(root): assert validate_registry(root)['passed']
def test_schema_count(root): assert validate_registry(root)['schema_count']>=20
def test_policy_count(root): assert validate_registry(root)['policy_count']>=20
def test_no_forbidden_mql5(root): assert not validate_registry(root)['forbidden_mql5_hits']
def test_delivery_valid(root): assert validate_delivery(root)['passed']
def test_acl14_dependency_doc(root): assert (root/'docs/alpha_lab_master_architecture/context_lifecycle_os/11_IMPLEMENTATION_PROGRAM/ACL_14_FIRST_REAL_CONTEXT_PILOT.md').is_file()
