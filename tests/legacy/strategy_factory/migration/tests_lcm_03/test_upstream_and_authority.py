import copy,pytest
from src.engine.tooling.strategy_factory.lcm.lcm_03.authority import build_permit,verify_permit
from src.engine.tooling.strategy_factory.lcm.lcm_03.errors import AuthorityError
from src.engine.tooling.strategy_factory.lcm.lcm_03.upstream import latest_classification,verify_classification

def test_upstream(repo_root): assert verify_classification(latest_classification(repo_root))['classification_id'].startswith('CLASSIFICATION_')
def test_permit(repo_root):
    up=verify_classification(latest_classification(repo_root));p=build_permit(up['handoff']['handoff_digest'],up['classification_id'],'2026-07-18T00:00:00Z');assert verify_permit(p,up['handoff']['handoff_digest'])
def test_permit_escalation_rejected(repo_root):
    up=verify_classification(latest_classification(repo_root));p=build_permit(up['handoff']['handoff_digest'],up['classification_id'],'2026-07-18T00:00:00Z');p['capabilities']['delete_source_files_allowed']=True
    with pytest.raises(AuthorityError): verify_permit(p,up['handoff']['handoff_digest'])
def test_permit_binding_rejected(repo_root):
    up=verify_classification(latest_classification(repo_root));p=build_permit(up['handoff']['handoff_digest'],up['classification_id'],'2026-07-18T00:00:00Z')
    with pytest.raises(AuthorityError): verify_permit(p,'sha256:bad')
