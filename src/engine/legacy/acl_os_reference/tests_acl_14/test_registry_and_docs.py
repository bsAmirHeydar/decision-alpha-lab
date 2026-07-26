from src.engine.tooling.strategy_factory.acl_os.acl_14.static_validation import validate_registry
from src.engine.tooling.strategy_factory.acl_os.acl_14.delivery_validation import validate_delivery
def test_static_registry(root): assert validate_registry(root)['passed']
def test_delivery(root): assert validate_delivery(root)['passed']
def test_canonical_docs(root): assert len(list((root/'docs/architecture/master/context_lifecycle_os/10_ONE_HOUR_CONTEXT').glob('ACL14_*.md')))>=30
def test_phase_docs(root): assert len(list((root/'docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_14').glob('*.md')))>=50
def test_atomic_docs(root): assert len(list((root/'docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_14').glob('*.md')))>=100
