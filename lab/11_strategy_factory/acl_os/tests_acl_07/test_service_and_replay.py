import json,shutil
from tools.strategy_factory.acl_os.acl_07.service import ACL07UnifiedValidationService
from tools.strategy_factory.acl_os.acl_07.replay_validator import verify_generated_root

def test_service_builds(acl06_root,permit,policy,tmp_path):
 d=tmp_path/'out'; r=ACL07UnifiedValidationService().validate(acl06_root,permit,policy,d,'2026-07-18T00:00:00Z'); assert d.exists() and r['validation_id']
def test_reference_decision_counts(acl06_root,permit,policy,tmp_path):
 d=tmp_path/'out'; r=ACL07UnifiedValidationService().validate(acl06_root,permit,policy,d,'2026-07-18T00:00:00Z'); assert r['decision_counts']['DIAGNOSTIC_EXCLUDED']==1 and r['decision_counts']['BASELINE_REFERENCE_ONLY']==4
def test_no_reporting_eligible_reference(acl06_root,permit,policy,tmp_path):
 d=tmp_path/'out'; r=ACL07UnifiedValidationService().validate(acl06_root,permit,policy,d,'2026-07-18T00:00:00Z'); assert r['decision_counts'].get('VALIDATION_ELIGIBLE_FOR_REPORTING',0)==0
def test_replay_validator_passes(acl06_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL07UnifiedValidationService().validate(acl06_root,permit,policy,d,'2026-07-18T00:00:00Z'); assert verify_generated_root(d)['passed']
def test_deterministic_replay(acl06_root,permit,policy,tmp_path):
 a=tmp_path/'a'; b=tmp_path/'b'; s=ACL07UnifiedValidationService(); ra=s.validate(acl06_root,permit,policy,a,'2026-07-18T00:00:00Z'); rb=s.validate(acl06_root,permit,policy,b,'2026-07-18T00:00:00Z'); assert ra['validation_id']==rb['validation_id']; assert (a/'decisions/validation_decision_bundle.json').read_bytes()==(b/'decisions/validation_decision_bundle.json').read_bytes()
def test_atomic_destination_rejects_nonempty(acl06_root,permit,policy,tmp_path):
 import pytest
 d=tmp_path/'out'; d.mkdir(); (d/'x').write_text('x')
 with pytest.raises(Exception): ACL07UnifiedValidationService().validate(acl06_root,permit,policy,d,'2026-07-18T00:00:00Z')
