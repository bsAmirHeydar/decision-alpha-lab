from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from strategy_factory_trainers_v3 import FoldDefinition, OOFProtocol, SplitRole

from .canonical import stable_id
from .config import SplitPolicy


@dataclass(frozen=True, slots=True)
class RowAssignment:
    event_id: str
    role: SplitRole
    fold_id: str


def _counts(total: int, fractions: tuple[float, ...]) -> list[int]:
    raw = [total * value for value in fractions]
    counts = [int(value) for value in raw]
    remainder = total - sum(counts)
    order = sorted(range(len(raw)), key=lambda index: (raw[index] - counts[index], -index), reverse=True)
    for index in order[:remainder]:
        counts[index] += 1
    positive = [index for index, fraction in enumerate(fractions) if fraction > 0]
    for index in positive:
        if counts[index] == 0 and total >= len(positive):
            donor = max(range(len(counts)), key=lambda j: counts[j])
            if counts[donor] > 1:
                counts[donor] -= 1
                counts[index] += 1
    return counts


def build_clustered_protocol(rows: list[tuple[str, int, str]], policy: SplitPolicy, task_id: str) -> tuple[dict[str, SplitRole], OOFProtocol]:
    clusters: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for event_id, event_time_ms, cluster_id in rows:
        clusters[cluster_id].append((event_id, event_time_ms))
    ordered_clusters = sorted(clusters, key=lambda key: (min(x[1] for x in clusters[key]), key))
    cluster_time = {key: min(x[1] for x in values) for key, values in clusters.items()}
    fractions = (
        policy.oof_train_fraction,
        policy.oof_calibration_fraction,
        policy.oof_threshold_fraction,
        policy.oof_holdout_fraction,
        policy.final_train_fraction,
        policy.final_calibration_fraction,
        policy.final_threshold_fraction,
        policy.final_test_fraction,
    )
    roles = (
        SplitRole.TRAIN,
        SplitRole.CALIBRATION,
        SplitRole.THRESHOLD,
        SplitRole.OOF_HOLDOUT,
        SplitRole.FINAL_TRAIN,
        SplitRole.FINAL_CALIBRATION,
        SplitRole.FINAL_THRESHOLD,
        SplitRole.FINAL_TEST,
    )
    counts = _counts(len(ordered_clusters), fractions)
    cluster_role: dict[str, SplitRole] = {}
    cursor = 0
    for role, count in zip(roles, counts):
        for cluster_id in ordered_clusters[cursor : cursor + count]:
            cluster_role[cluster_id] = role
        cursor += count

    def apply_purge_before(test_role: SplitRole, eligible_roles: set[SplitRole]) -> None:
        test_clusters = [key for key, role in cluster_role.items() if role is test_role]
        if not test_clusters or policy.purge_ms <= 0:
            return
        boundary = min(cluster_time[key] for key in test_clusters)
        for key, role in list(cluster_role.items()):
            if role in eligible_roles and boundary - policy.purge_ms <= cluster_time[key] < boundary:
                cluster_role[key] = SplitRole.PURGED

    def apply_embargo_after(test_role: SplitRole, eligible_roles: set[SplitRole]) -> None:
        test_clusters = [key for key, role in cluster_role.items() if role is test_role]
        if not test_clusters or policy.embargo_ms <= 0:
            return
        boundary = max(cluster_time[key] for key in test_clusters)
        for key, role in list(cluster_role.items()):
            if role in eligible_roles and boundary < cluster_time[key] <= boundary + policy.embargo_ms:
                cluster_role[key] = SplitRole.EMBARGO

    apply_purge_before(SplitRole.OOF_HOLDOUT, {SplitRole.TRAIN, SplitRole.CALIBRATION, SplitRole.THRESHOLD})
    apply_embargo_after(SplitRole.OOF_HOLDOUT, {SplitRole.FINAL_TRAIN, SplitRole.FINAL_CALIBRATION, SplitRole.FINAL_THRESHOLD})
    apply_purge_before(SplitRole.FINAL_TEST, {SplitRole.FINAL_TRAIN, SplitRole.FINAL_CALIBRATION, SplitRole.FINAL_THRESHOLD})

    assignments: dict[str, SplitRole] = {}
    role_ids: dict[SplitRole, list[str]] = {role: [] for role in (*roles, SplitRole.PURGED, SplitRole.EMBARGO)}
    for cluster_id in ordered_clusters:
        role = cluster_role[cluster_id]
        for event_id, _ in clusters[cluster_id]:
            assignments[event_id] = role
            role_ids[role].append(event_id)

    required = (SplitRole.TRAIN, SplitRole.OOF_HOLDOUT, SplitRole.FINAL_TRAIN, SplitRole.FINAL_TEST)
    if any(not role_ids[role] for role in required):
        raise ValueError(f"insufficient independent clusters for governed split after purge/embargo: {task_id}")
    fold = FoldDefinition(
        "fold_000",
        tuple(role_ids[SplitRole.TRAIN]),
        tuple(role_ids[SplitRole.CALIBRATION]),
        tuple(role_ids[SplitRole.THRESHOLD]),
        tuple(role_ids[SplitRole.OOF_HOLDOUT]),
        tuple(role_ids[SplitRole.PURGED]),
        tuple(role_ids[SplitRole.EMBARGO]),
    )
    material = {role.value: sorted(ids) for role, ids in role_ids.items()}
    protocol = OOFProtocol(
        stable_id("rthp_oof_", {"task": task_id, "roles": material}, 24),
        "1.0.0",
        (fold,),
        tuple(role_ids[SplitRole.FINAL_TRAIN]),
        tuple(role_ids[SplitRole.FINAL_CALIBRATION]),
        tuple(role_ids[SplitRole.FINAL_THRESHOLD]),
        tuple(role_ids[SplitRole.FINAL_TEST]),
        True,
        policy.purge_ms,
        policy.embargo_ms,
    )
    return assignments, protocol
