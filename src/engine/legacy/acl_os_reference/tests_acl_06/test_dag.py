from collections import Counter
from tools.strategy_factory.acl_os.acl_06.dag import topological_order
def test_dag_is_closed_and_acyclic(build):
    d=build()['dag']; assert d['closed'] and len(topological_order(d))==d['task_count']
def test_expected_task_shape(build):
    c=Counter(t['task_type'] for t in build()['dag']['tasks']); assert c['EVALUATE_CANDIDATE_SEGMENT']==36 and c['AGGREGATE_CANDIDATE']==12
def test_every_task_is_deterministic_and_idempotent(build): assert all(t['deterministic'] and t['idempotent'] for t in build()['dag']['tasks'])
def test_task_cache_keys_are_unique(build):
    keys=[t['cache_key'] for t in build()['dag']['tasks']]; assert len(keys)==len(set(keys))
