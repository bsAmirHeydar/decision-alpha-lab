import json
from tools.strategy_factory.acl_os.acl_10.replay_validator import verify_generated_root
from tools.strategy_factory.acl_os.acl_10.service import ACL10PromotionStateService

def test_reference_replay(reference): assert verify_generated_root(reference)['passed']
def test_service_build(tmp_path,acl09_root,permit,policy):
    out=tmp_path/'out'; result=ACL10PromotionStateService().build(acl09_root,permit,policy,out,'2026-07-18T03:00:00Z'); assert result['passed']; assert result['promotion_review_eligible_count']==0; assert verify_generated_root(out)['passed']
def test_deterministic_outputs(tmp_path,acl09_root,permit,policy):
    a=tmp_path/'a'; b=tmp_path/'b'; service=ACL10PromotionStateService(); service.build(acl09_root,permit,policy,a,'2026-07-18T03:00:00Z'); service.build(acl09_root,permit,policy,b,'2026-07-18T03:00:00Z')
    assert json.loads((a/'run/promotion_run.json').read_text())==json.loads((b/'run/promotion_run.json').read_text())
    assert json.loads((a/'decisions/promotion_decision_bundle.json').read_text())==json.loads((b/'decisions/promotion_decision_bundle.json').read_text())
def test_runtime_manifest_empty(reference):
    d=json.loads((reference/'runtime/runtime_candidate_manifest.json').read_text()); assert d['runtime_candidate_count']==0 and d['runtime_generation_allowed'] is False
def test_approval_requests_empty(reference):
    d=json.loads((reference/'approval/approval_request_bundle.json').read_text()); assert d['approval_request_count']==0 and d['self_approval_allowed'] is False
def test_acl11_handoff_non_executable(reference):
    d=json.loads((reference/'handoff/acl11_handoff.json').read_text()); assert d['runtime_candidate_count']==0 and d['runtime_generation_allowed'] is False and d['capital_activation_allowed'] is False
