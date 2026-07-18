from tools.strategy_factory.acl_os.acl_09.delivery_validator import validate_delivery
from tools.strategy_factory.acl_os.acl_09.static_validator import validate_registry_files

def test_registry_files_valid():
    r=validate_registry_files()
    assert r['passed'] and r['schema_count']>=20 and r['policy_count']>=20 and r['question_count']==8

def test_delivery(repo_root):
    assert validate_delivery(repo_root)['passed']

def test_mql_guards_present(repo_root):
    root=repo_root/'lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL09'
    text='\n'.join(p.read_text() for p in root.glob('*.mqh'))
    assert 'ACL09_RESEARCH_EXECUTION_ALLOWED false' in text
    assert 'ACL09_LIVE_ORDER_SUBMISSION_ALLOWED false' in text
    assert 'ACL09_CAPITAL_ACTIVATION_ALLOWED false' in text

def test_docs_are_present(repo_root):
    root=repo_root/'docs/alpha_lab_master_architecture/context_lifecycle_os'
    assert (root/'12_PHASE_DELIVERIES/ACL_09/00_MOC.md').exists()
    assert (root/'13_ATOMIC_CONCEPTS/ACL_09/000_MOC.md').exists()
