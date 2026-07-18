from tools.strategy_factory.lcm.lcm_02.ownership import family_roles,owner_binding
from tools.strategy_factory.lcm.lcm_02.authority import build_permit,verify_permit
import pytest

def test_role_registry_has_no_invented_human():
 r=family_roles(['EXP0018_DAYE_TRADER']); assert not r['human_approval_claimed']; assert any(x['assignee_id'] is None for x in r['roles'])
def test_security_owner_required():
 b=owner_binding('EXP0018_DAYE_TRADER','EXECUTION_ADAPTER',True); assert b['security_reviewer_role']=='SECURITY_REVIEWER'; assert not b['ownership_is_human_approved']
def test_permit_denies_destructive_authority():
 p=build_permit('sha256:'+'a'*64,'SURVEY_X','2026-07-18T00:00:00Z'); assert verify_permit(p,'sha256:'+'a'*64); assert not p['capabilities']['delete_source_files_allowed']
def test_tampered_permit_rejected():
 p=build_permit('sha256:'+'a'*64,'SURVEY_X','2026-07-18T00:00:00Z'); p['capabilities']['delete_source_files_allowed']=True
 with pytest.raises(Exception): verify_permit(p,'sha256:'+'a'*64)
