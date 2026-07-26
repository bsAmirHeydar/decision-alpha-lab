import json,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_08.service import ACL08ReportingExperienceService
from src.engine.tooling.strategy_factory.acl_os.acl_08.replay_validator import verify_generated_root

def test_service_builds(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; r=ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); assert d.exists() and r['report_id'] and r['artifact_count']>0
def test_replay_validator_passes(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); assert verify_generated_root(d)['passed']
def test_deterministic_replay(acl07_root,permit,policy,tmp_path):
 a=tmp_path/'a'; b=tmp_path/'b'; s=ACL08ReportingExperienceService(); ra=s.build(acl07_root,permit,policy,a,'2026-07-18T01:00:00Z'); rb=s.build(acl07_root,permit,policy,b,'2026-07-18T01:00:00Z'); assert ra['report_id']==rb['report_id']; assert (a/'reports/batch_report.json').read_bytes()==(b/'reports/batch_report.json').read_bytes()
def test_atomic_destination_rejects_nonempty(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; d.mkdir(); (d/'x').write_text('x')
 with pytest.raises(Exception): ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z')
def test_handoff_has_no_authority(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); h=json.loads((d/'handoff/acl09_handoff.json').read_text()); assert not h['alpha_claim_allowed'] and not h['promotion_allowed'] and not h['live_order_submission_allowed'] and not h['capital_activation_allowed']
def test_event_chain_has_seven_events(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); e=json.loads((d/'events/report_event_ledger.json').read_text()); assert e['event_count']==7
