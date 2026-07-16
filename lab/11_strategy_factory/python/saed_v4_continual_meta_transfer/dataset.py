from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Iterable

from .budget import ResearchLedger
from .canonical import content_hash, seal, stable_id
from .contracts import MetaDatasetContract, REQUIRED_TASK_FIELDS
from .errors import ContractError, KnownTimeError


def _time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"invalid {label}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _matrix(value, columns: int, label: str) -> list[list[float]]:
    output = []
    for row in value:
        row_values = [float(item) for item in row]
        if len(row_values) != columns:
            raise ContractError(f"{label} column mismatch")
        output.append(row_values)
    if not output:
        raise ContractError(f"{label} cannot be empty")
    return output


def validate(tasks: Iterable[dict], contract: MetaDatasetContract, ledger: ResearchLedger) -> dict:
    tasks = [dict(task) for task in tasks]
    ledger.consume("tasks", len(tasks), "meta dataset validation")
    if len(tasks) < contract.minimum_tasks:
        raise ContractError("insufficient meta tasks")
    ids = set()
    role_counts = Counter()
    context_counts = Counter()
    cluster_roles: dict[str, set[str]] = defaultdict(set)
    chronological = []
    feature_count = len(contract.feature_names)
    parameter_count = len(contract.parameter_names)
    for task in tasks:
        if set(task) != REQUIRED_TASK_FIELDS:
            raise ContractError(f"task field mismatch: {sorted(set(task) ^ REQUIRED_TASK_FIELDS)}")
        task_id = str(task["task_id"])
        if not task_id or task_id in ids:
            raise ContractError("empty or duplicate task_id")
        ids.add(task_id)
        role = str(task["role"])
        if role not in set(contract.allowed_roles):
            raise ContractError("unknown task role")
        role_counts[role] += 1
        context_id = str(task["context_id"])
        cluster_id = str(task["cluster_id"])
        regime = str(task["regime"])
        if not context_id or not cluster_id or not regime:
            raise ContractError("empty task identity")
        context_counts[context_id] += 1
        cluster_roles[cluster_id].add(role)
        start = _time(task["window_start"], "window_start")
        decision = _time(task["decision_time"], "decision_time")
        end = _time(task["window_end"], "window_end")
        known = _time(task["feature_known_at"], "feature_known_at")
        observed = _time(task["outcome_observed_at"], "outcome_observed_at")
        if not (start <= known <= decision <= end <= observed):
            raise KnownTimeError(f"known-time ordering violated for {task_id}")
        if bool(task["future_suffix_accessed"]):
            raise KnownTimeError(f"future suffix accessed for {task_id}")
        if bool(task["protected_evidence_accessed"]):
            raise KnownTimeError(f"protected evidence accessed for {task_id}")
        summary = [float(item) for item in task["feature_summary"]]
        if len(summary) != feature_count:
            raise ContractError("feature summary dimension mismatch")
        support_features = _matrix(task["support_features"], feature_count, "support_features")
        support_targets = [float(item) for item in task["support_targets"]]
        if len(support_features) != len(support_targets):
            raise ContractError("support rows and targets mismatch")
        query_features = _matrix(task["query_features"], feature_count, "query_features")
        query_targets = [float(item) for item in task["query_targets"]]
        if len(query_features) != len(query_targets):
            raise ContractError("query rows and targets mismatch")
        parameters = [float(item) for item in task["baseline_parameters"]]
        if len(parameters) != parameter_count:
            raise ContractError("parameter dimension mismatch")
        support_score = float(task["support_score"])
        ood_pvalue = float(task["ood_pvalue"])
        if not (0.0 <= support_score <= 1.0 and 0.0 <= ood_pvalue <= 1.0):
            raise ContractError("support or OOD probability outside domain")
        float(task["conformal_value_lower_bound"])
        chronological.append((decision, task_id))
    if len(context_counts) < contract.minimum_contexts:
        raise ContractError("insufficient contexts")
    if len(cluster_roles) < contract.minimum_clusters:
        raise ContractError("insufficient clusters")
    if any(count < contract.minimum_tasks_per_role for count in role_counts.values()) or set(role_counts) != set(contract.allowed_roles):
        raise ContractError("insufficient tasks per role")
    if contract.cluster_role_separation_required and any(len(roles) != 1 for roles in cluster_roles.values()):
        raise ContractError("cluster appears in more than one role")
    if contract.strict_chronology and chronological != sorted(chronological):
        raise ContractError("tasks are not strictly chronological")
    payload = {
        "phase": "SAED_V4_25",
        "task_count": len(tasks),
        "context_count": len(context_counts),
        "cluster_count": len(cluster_roles),
        "role_counts": dict(sorted(role_counts.items())),
        "context_counts": dict(sorted(context_counts.items())),
        "feature_names": list(contract.feature_names),
        "parameter_names": list(contract.parameter_names),
        "strict_chronology": True,
        "cluster_role_separation": True,
        "query_outcomes_protected_during_adaptation": True,
        "future_suffix_queries": 0,
        "protected_evidence_queries": 0,
        "dataset_hash": content_hash(tasks),
    }
    payload["dataset_id"] = stable_id("meta_dataset", payload)
    return seal(payload, "summary_hash")


def by_role(tasks: Iterable[dict]) -> dict[str, list[dict]]:
    output = {role: [] for role in sorted({"meta_train", "meta_validation", "transfer_test", "drift_reference"})}
    for task in tasks:
        output[str(task["role"])].append(dict(task))
    return output
