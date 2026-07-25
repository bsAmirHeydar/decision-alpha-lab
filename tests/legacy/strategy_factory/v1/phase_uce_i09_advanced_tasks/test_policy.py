from strategy_factory_advanced_tasks_v3.golden import policy_rows
from strategy_factory_advanced_tasks_v3.policy import *
def test_policy_never_generates_unseen_action_and_has_support_gate():
 rows,actions=policy_rows();a=audit_policy_support(rows,actions,5,.01);assert a.decision.value=='accept';m=ConservativePolicyImprovement(actions,5,1.,0).fit(rows);d=m.decide(rows[0],'wide_stop');assert d.selected_action_key in actions

def test_unseen_action_blocks_support():
 rows,actions=policy_rows();a=audit_policy_support(rows,actions+('unseen',),5,.01);assert a.decision.value=='reject';assert 'unseen' in a.unseen_action_keys
