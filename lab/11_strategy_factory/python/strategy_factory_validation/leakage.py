from __future__ import annotations
from collections import defaultdict
from .models import ValidationFold, FoldObservation, LeakageFinding
from .enums import FoldRole, LeakageSeverity
from .hashing import stable_id

def audit_fold_observations(folds: tuple[ValidationFold, ...],
                            observations: tuple[FoldObservation, ...],
                            forbid_cluster_cross_role: bool = True) -> tuple[LeakageFinding, ...]:
    by_fold = {f.fold_id: f for f in folds}
    findings: list[LeakageFinding] = []
    seen_identity: set[str] = set()
    cluster_roles: dict[tuple[str, str], set[FoldRole]] = defaultdict(set)
    for row in observations:
        try:
            row.validate()
        except ValueError as exc:
            findings.append(_finding(LeakageSeverity.FATAL, "INVALID_OBSERVATION",
                                     row.fold_id, row.trial_id, row.event_id, str(exc)))
            continue
        if row.observation_id in seen_identity:
            findings.append(_finding(LeakageSeverity.FATAL, "DUPLICATE_OBSERVATION",
                                     row.fold_id, row.trial_id, row.event_id,
                                     "observation_id appears more than once"))
        seen_identity.add(row.observation_id)
        fold = by_fold.get(row.fold_id)
        if fold is None:
            findings.append(_finding(LeakageSeverity.FATAL, "UNKNOWN_FOLD",
                                     row.fold_id, row.trial_id, row.event_id,
                                     "observation references an undeclared fold"))
            continue
        expected_range = {FoldRole.TRAIN: fold.train,
                          FoldRole.VALIDATION: fold.validation,
                          FoldRole.TEST: fold.test}.get(row.role)
        if expected_range is None:
            findings.append(_finding(LeakageSeverity.FATAL, "NON_EVALUATION_ROLE",
                                     row.fold_id, row.trial_id, row.event_id,
                                     "purged or embargo observations cannot enter metrics"))
        elif not expected_range.contains(row.known_time_utc_msc):
            findings.append(_finding(LeakageSeverity.FATAL, "KNOWN_TIME_OUTSIDE_ROLE",
                                     row.fold_id, row.trial_id, row.event_id,
                                     "known_time is outside the declared role range"))
        if row.resolved_time_utc_msc < row.known_time_utc_msc:
            findings.append(_finding(LeakageSeverity.FATAL, "NEGATIVE_CAUSAL_ORDER",
                                     row.fold_id, row.trial_id, row.event_id,
                                     "resolved_time precedes known_time"))
        cluster_roles[(row.fold_id, row.cluster_id)].add(row.role)
    if forbid_cluster_cross_role:
        for (fold_id, cluster_id), roles in sorted(cluster_roles.items()):
            eval_roles = roles & {FoldRole.TRAIN, FoldRole.VALIDATION, FoldRole.TEST}
            if len(eval_roles) > 1:
                findings.append(_finding(LeakageSeverity.FATAL, "CLUSTER_CROSSES_ROLE",
                                         fold_id, "*", cluster_id,
                                         "one market-event cluster appears in multiple fold roles"))
    return tuple(findings)

def assert_no_fatal_leakage(findings: tuple[LeakageFinding, ...]) -> None:
    fatal = [x for x in findings if x.severity == LeakageSeverity.FATAL]
    if fatal:
        codes = ", ".join(sorted({x.code for x in fatal}))
        raise ValueError(f"fatal leakage findings: {codes}")

def _finding(severity, code, fold_id, trial_id, event_id, detail):
    payload = f"{int(severity)}|{code}|{fold_id}|{trial_id}|{event_id}|{detail}"
    return LeakageFinding(stable_id("leak", payload), severity, code,
                          fold_id, trial_id, event_id, detail)
