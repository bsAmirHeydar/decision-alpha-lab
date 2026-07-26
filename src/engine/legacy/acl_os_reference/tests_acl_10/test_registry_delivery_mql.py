from src.engine.tooling.strategy_factory.acl_os.acl_10.delivery_validator import validate_delivery
from src.engine.tooling.strategy_factory.acl_os.acl_10.static_validator import validate_registry_files

def test_static_registry():
    r=validate_registry_files(); assert r['passed'] and r['schema_count']>=30 and r['policy_count']>=25
def test_delivery(repo): assert validate_delivery(repo)['passed']
def test_mql_aggregate_exists(repo): assert (repo/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL10/ACL10.mqh').is_file()
def test_docs_exist(repo): assert (repo/'docs/architecture/master/context_lifecycle_os/12_OPERATIONS/ACL10_PROMOTION_STATE_MACHINE_RUNTIME.md').is_file()
