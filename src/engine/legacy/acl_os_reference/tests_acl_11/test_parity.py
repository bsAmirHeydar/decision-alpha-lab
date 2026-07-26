from src.engine.tooling.strategy_factory.acl_os.acl_11.handoff_input import load_acl10_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_11.registries import parity_registry,custody_state_registry
from src.engine.tooling.strategy_factory.acl_os.acl_11.parity import assess
def test_registry_closed():
    r=parity_registry(); assert r['closed'] and len(r['requirements'])==20
def test_no_candidate_assessment(acl10):
    a=assess(load_acl10_bundle(acl10),parity_registry(),'2026-07-18T04:00:00Z'); assert a['runtime_candidate_count']==0 and not a['all_hard_requirements_satisfied']
def test_only_integrity_satisfied_without_candidate(acl10):
    a=assess(load_acl10_bundle(acl10),parity_registry(),'2026-07-18T04:00:00Z'); assert a['status_counts']['SATISFIED']==1 and a['status_counts']['UNSATISFIED']==1
def test_custody_registry_never_executable(): assert all(not x['runtime_executable'] for x in custody_state_registry()['states'])
