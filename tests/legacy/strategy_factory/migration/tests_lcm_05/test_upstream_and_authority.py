import copy,pytest
from tools.strategy_factory.lcm.lcm_05.upstream import load
from tools.strategy_factory.lcm.lcm_05.authority import build_permit,verify_permit
from tools.strategy_factory.lcm.lcm_05.errors import PolicyError

def test_lcm04_handoff_bound(repo_root):
    up=load(repo_root);assert up['handoff']['handoff_type']=='LCM04_TO_LCM05'
def test_permit_valid(repo_root):
    up=load(repo_root);p=build_permit(up['handoff']['handoff_digest'],up['marker']['characterization_run_id'],'2026-07-19T00:00:00Z');assert verify_permit(p,up['handoff']['handoff_digest'])
def test_permit_denies_materialization(repo_root):
    up=load(repo_root);p=build_permit(up['handoff']['handoff_digest'],up['marker']['characterization_run_id'],'2026-07-19T00:00:00Z');assert p['target_materialization_allowed'] is False
def test_permit_tamper_fails(repo_root):
    up=load(repo_root);p=build_permit(up['handoff']['handoff_digest'],up['marker']['characterization_run_id'],'2026-07-19T00:00:00Z');p['source_move_allowed']=True
    with pytest.raises(PolicyError):verify_permit(p,up['handoff']['handoff_digest'])
