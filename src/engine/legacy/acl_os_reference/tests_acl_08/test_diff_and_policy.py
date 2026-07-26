import copy,json,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_08.report_policy import validate_policy
from src.engine.tooling.strategy_factory.acl_os.acl_08.service import ACL08ReportingExperienceService

def test_policy_valid(policy): assert validate_policy(policy)['policy_id']=='ACL08_REPORT_POLICY_V1'
def test_policy_digest_tamper_rejected(policy):
 p=copy.deepcopy(policy); p['max_executive_findings']=99
 with pytest.raises(Exception): validate_policy(p)
def test_registry_order_tamper_rejected(policy):
 p=copy.deepcopy(policy); p['report_blocks']=list(reversed(p['report_blocks']))
 with pytest.raises(Exception): validate_policy(p)
def test_first_report_diff(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); x=json.loads((d/'reports/report_diff.json').read_text()); assert x['comparison_status']=='FIRST_REPORT' and not x['material_change']
def test_same_report_diff_no_material_change(acl07_root,permit,policy,tmp_path):
 a=tmp_path/'a'; b=tmp_path/'b'; s=ACL08ReportingExperienceService(); s.build(acl07_root,permit,policy,a,'2026-07-18T01:00:00Z'); s.build(acl07_root,permit,policy,b,'2026-07-18T02:00:00Z',a); x=json.loads((b/'reports/report_diff.json').read_text()); assert x['comparison_status']=='NO_MATERIAL_CHANGE'
