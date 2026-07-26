import json,shutil,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_08.replay_validator import verify_generated_root
from src.engine.tooling.strategy_factory.acl_os.acl_08.service import ACL08ReportingExperienceService

def build(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); return d
def test_manifest_detects_tamper(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); p=d/'reports/batch_report.json'; p.write_text(p.read_text()+' '); assert not verify_generated_root(d)['passed']
def test_external_view_contains_claim_ceiling(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); x=json.loads((d/'views/external_restricted.json').read_text()); assert x['claim_ceiling']=='REPORTING_AND_EXPERIENCE_REFERENCE_ONLY'
def test_docs_do_not_claim_alpha(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); text=(d/'docs/ACL08_REPORTING_SUMMARY.md').read_text(); assert 'no alpha' in text.lower() and 'capital authority' in text.lower()
def test_no_network_or_secret_capability(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); x=json.loads((d/'security/security_boundary_report.json').read_text()); assert not x['network_access_allowed'] and not x['secret_access_allowed']
