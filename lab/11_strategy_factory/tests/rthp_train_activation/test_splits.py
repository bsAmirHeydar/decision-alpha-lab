from __future__ import annotations

from strategy_factory_rthp_train_activation_v1.config import SplitPolicy
from strategy_factory_rthp_train_activation_v1.splits import build_clustered_protocol
from strategy_factory_trainers_v3 import SplitRole


def test_purge_and_embargo_are_applied_without_cluster_leakage():
    rows = [(f"e{i}", i * 1000, f"c{i}") for i in range(80)]
    policy = SplitPolicy(8, 0.20, 0.05, 0.05, 0.10, 0.35, 0.05, 0.05, 0.15, 2000, 2000)
    assignments, protocol = build_clustered_protocol(rows, policy, "task")
    assert protocol.test_sealed is True
    assert protocol.purge_ms == 2000
    assert protocol.embargo_ms == 2000
    assert SplitRole.PURGED in set(assignments.values())
    assert SplitRole.EMBARGO in set(assignments.values())
    by_cluster = {}
    for event_id, _, cluster_id in rows:
        by_cluster.setdefault(cluster_id, set()).add(assignments[event_id])
    assert all(len(roles) == 1 for roles in by_cluster.values())
