import json
from tools.strategy_factory.acl_os.acl_07.delivery_validator import validate_delivery
from tools.strategy_factory.acl_os.acl_07.static_validator import validate_registry_files

def test_registry_files_valid(): assert validate_registry_files()['passed']
def test_schema_count(): assert validate_registry_files()['schema_count']>=18
def test_policy_count(): assert validate_registry_files()['policy_count']>=20
def test_reference_handoff_denies_execution(repo_root):
 h=json.loads((repo_root/'lab/11_strategy_factory/acl_os/fixtures/acl_07/reference_validation/handoff/acl08_handoff.json').read_text()); assert not h['live_order_submission_allowed'] and not h['capital_activation_allowed']
def test_reference_diagnostic_not_promoted(repo_root):
 r=json.loads((repo_root/'lab/11_strategy_factory/acl_os/fixtures/acl_07/reference_validation/reports/diagnostic_isolation_report.json').read_text()); assert r['passed'] and not r['diagnostic_promoted']
def test_delivery(repo_root): assert validate_delivery(repo_root)['passed']
