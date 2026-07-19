from tools.strategy_factory.lcm.lcm_04.upstream import latest_identity,verify_identity
from tools.strategy_factory.lcm.lcm_04.authority import build_permit,verify_permit

def test_upstream_integrity(repo_root): assert verify_identity(latest_identity(repo_root))['handoff']['handoff_type']=='LCM03_TO_LCM04'
def test_permit_denies_legacy_execution(repo_root):
    up=verify_identity(latest_identity(repo_root));p=build_permit(up['handoff']['handoff_digest'],up['marker']['identity_run_id'],'2026-07-19T00:00:00Z')
    assert verify_permit(p,up['handoff']['handoff_digest']) and not p['legacy_trace_execution_allowed']
