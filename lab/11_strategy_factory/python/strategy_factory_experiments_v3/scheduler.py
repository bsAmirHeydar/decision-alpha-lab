"""Deterministic dependency-aware local scheduler for UCE-I11.

The reference scheduler executes sequentially to make event ordering bit-exact.
The resource-claim and worker-isolation contracts are still explicit, allowing a
parallel/process implementation to replace the executor without changing DAG,
ledger, retry, cancellation, or budget semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Mapping

from .budget import BudgetManager
from .canonical import canonical_sha256, stable_id
from .contracts import (
    DagNode,
    ExperimentManifest,
    ResourceClaim,
    SchedulerEvent,
    WorkResult,
)
from .enums import (
    BudgetDecision,
    FailureDisposition,
    LedgerAction,
    NodeStatus,
    SchedulerEventKind,
)
from .errors import ExperimentError
from .ledger import SelectionLedger

Worker = Callable[[DagNode, int, str], WorkResult]
CacheResolver = Callable[[DagNode], WorkResult | None]


@dataclass(frozen=True, slots=True)
class SchedulerRun:
    manifest_hash: str
    statuses: Mapping[str, NodeStatus]
    attempts: Mapping[str, int]
    events: tuple[SchedulerEvent, ...]
    event_stream_hash: str
    ledger_entries: tuple
    budget_usage: object
    completed: bool
    blockers: tuple[str, ...]


class DeterministicScheduler:
    def __init__(self, version: str = "1.0.0", environment_hash: str | None = None) -> None:
        self.version = version
        self.environment_hash = environment_hash or canonical_sha256(
            {"scheduler": "uce_i11_reference", "version": version, "mode": "sequential_isolated_contract"}
        )

    def run(
        self,
        manifest: ExperimentManifest,
        budget_manager: BudgetManager,
        worker: Worker,
        *,
        cancelled_node_ids: frozenset[str] = frozenset(),
        cache_resolver: CacheResolver | None = None,
        resume_statuses: Mapping[str, NodeStatus] | None = None,
    ) -> SchedulerRun:
        if manifest.scheduler_version != self.version:
            raise ExperimentError(
                "scheduler_version_mismatch",
                "manifest scheduler_version differs from active scheduler",
                {"manifest": manifest.scheduler_version, "active": self.version},
            )
        if manifest.trials and any(trial.budget_policy_hash != budget_manager.policy.policy_hash for trial in manifest.trials):
            raise ExperimentError(
                "scheduler_budget_policy_mismatch",
                "scheduler budget policy differs from the policy compiled into trial identity",
            )
        statuses = {node.node_id: NodeStatus.PLANNED for node in manifest.nodes}
        attempts = {node.node_id: 0 for node in manifest.nodes}
        events: list[SchedulerEvent] = []
        ledger = SelectionLedger(
            experiment_id=self._experiment_id(manifest),
            manifest_hash=manifest.manifest_hash,
        )
        node_by_id = {node.node_id: node for node in manifest.nodes}
        claim_by_hash = {claim.claim_hash: claim for claim in manifest.resource_claims}
        trial_by_id = {trial.trial_id: trial for trial in manifest.trials}
        terminal_failure = {
            NodeStatus.FAILED,
            NodeStatus.TIMED_OUT,
            NodeStatus.CANCELLED,
            NodeStatus.QUARANTINED,
            NodeStatus.INVALID,
            NodeStatus.SKIPPED,
            NodeStatus.PRUNED,
        }

        def emit(
            node: DagNode,
            kind: SchedulerEventKind,
            before: NodeStatus,
            after: NodeStatus,
            attempt: int,
            worker_id: str,
            reason_code: str,
            extra: Mapping | None = None,
        ) -> SchedulerEvent:
            payload = {
                "sequence": len(events),
                "node_id": node.node_id,
                "trial_id": node.trial_id,
                "kind": kind.value,
                "status_before": before.value,
                "status_after": after.value,
                "attempt": attempt,
                "worker_id": worker_id,
                "reason_code": reason_code,
                "environment_hash": self.environment_hash,
                "extra": dict(extra or {}),
            }
            event = SchedulerEvent(
                event_id=stable_id("uceschevent", payload),
                sequence=len(events),
                node_id=node.node_id,
                trial_id=node.trial_id,
                kind=kind,
                status_before=before,
                status_after=after,
                attempt=attempt,
                worker_id=worker_id,
                payload_hash=canonical_sha256(payload),
                reason_code=reason_code,
            )
            events.append(event)
            statuses[node.node_id] = after
            return event

        def append_ledger(node: DagNode, action: LedgerAction, reason: str, result: WorkResult | None = None) -> None:
            ledger.append(
                trial_id=node.trial_id or f"meta:{manifest.manifest_id}",
                node_id=node.node_id,
                action=action,
                reason_code=reason,
                metrics=(result.metrics if result else {}),
                artifact_hashes=(result.artifact_hashes if result else ()),
            )

        pending = set(node_by_id)
        for node_id, resumed_status in sorted((resume_statuses or {}).items()):
            if node_id not in node_by_id:
                raise ExperimentError("resume_unknown_node", "resume snapshot references unknown node", {"node_id": node_id})
            if resumed_status not in (NodeStatus.SUCCEEDED, NodeStatus.CACHED):
                raise ExperimentError("resume_non_success_status", "only succeeded/cached nodes may be resumed", {"status": resumed_status.value})
            node = node_by_id[node_id]
            emit(node, SchedulerEventKind.RESUME, NodeStatus.PLANNED, resumed_status, 0, "", "validated_resume_snapshot")
            append_ledger(node, LedgerAction.RESUMED, "validated_resume_snapshot")
            pending.remove(node_id)

        while pending:
            progress = False
            ready = sorted(
                (
                    node_by_id[node_id]
                    for node_id in pending
                    if all(statuses[parent] in (NodeStatus.SUCCEEDED, NodeStatus.CACHED) for parent in node_by_id[node_id].dependencies)
                ),
                key=lambda node: (node.priority, node.node_id),
            )

            # Nodes whose dependencies are terminal failures can never become ready.
            blocked = sorted(
                (
                    node_by_id[node_id]
                    for node_id in pending
                    if any(statuses[parent] in terminal_failure for parent in node_by_id[node_id].dependencies)
                ),
                key=lambda node: (node.priority, node.node_id),
            )
            for node in blocked:
                emit(node, SchedulerEventKind.SKIP, statuses[node.node_id], NodeStatus.SKIPPED, 0, "", "dependency_terminal")
                append_ledger(node, LedgerAction.SKIPPED, "dependency_terminal")
                pending.remove(node.node_id)
                progress = True

            for node in ready:
                if node.node_id not in pending:
                    continue
                progress = True
                if node.node_id in cancelled_node_ids:
                    emit(node, SchedulerEventKind.CANCEL, statuses[node.node_id], NodeStatus.CANCELLED, 0, "", "explicit_cancellation")
                    append_ledger(node, LedgerAction.CANCELLED, "explicit_cancellation")
                    pending.remove(node.node_id)
                    continue

                emit(node, SchedulerEventKind.READY, statuses[node.node_id], NodeStatus.READY, attempts[node.node_id], "", "dependencies_satisfied")

                cached = cache_resolver(node) if cache_resolver is not None else None
                if cached is not None:
                    if cached.status is not NodeStatus.CACHED:
                        raise ExperimentError("invalid_cache_resolver_result", "cache resolver must return CACHED WorkResult")
                    emit(node, SchedulerEventKind.CACHE_HIT, NodeStatus.READY, NodeStatus.CACHED, attempts[node.node_id], "", "valid_content_cache", {"artifacts": cached.artifact_hashes})
                    append_ledger(node, LedgerAction.CACHED, "valid_content_cache", cached)
                    pending.remove(node.node_id)
                    continue

                claim: ResourceClaim | None = None
                if node.resource_claim_hash:
                    claim = claim_by_hash.get(node.resource_claim_hash)
                    if claim is None:
                        emit(node, SchedulerEventKind.QUARANTINE, NodeStatus.READY, NodeStatus.QUARANTINED, 0, "", "resource_claim_missing")
                        append_ledger(node, LedgerAction.INVALID, "resource_claim_missing")
                        pending.remove(node.node_id)
                        continue
                    trial = trial_by_id[node.trial_id]
                    assessment = budget_manager.reserve(claim, trial.candidate_key)
                    if assessment.decision is BudgetDecision.DENY:
                        reason = assessment.reason_codes[0]
                        emit(node, SchedulerEventKind.SKIP, NodeStatus.READY, NodeStatus.SKIPPED, 0, "", reason)
                        append_ledger(node, LedgerAction.SKIPPED, reason)
                        pending.remove(node.node_id)
                        continue
                    emit(node, SchedulerEventKind.CLAIM, NodeStatus.READY, NodeStatus.READY, 0, "", "resource_claim_reserved", {"assessment_hash": assessment.assessment_hash})

                terminal = False
                while not terminal:
                    attempts[node.node_id] += 1
                    attempt = attempts[node.node_id]
                    worker_id = stable_id("uceworker", {"node_id": node.node_id, "attempt": attempt, "environment_hash": self.environment_hash}, 16)
                    emit(node, SchedulerEventKind.START, statuses[node.node_id], NodeStatus.RUNNING, attempt, worker_id, "isolated_worker_start")
                    append_ledger(node, LedgerAction.ATTEMPTED, "isolated_worker_start")
                    try:
                        result = worker(node, attempt, worker_id)
                    except Exception as exc:  # scheduler must preserve unexpected failures as evidence
                        result = WorkResult(
                            status=NodeStatus.FAILED,
                            failure_code=f"worker_exception:{type(exc).__name__}",
                            failure_disposition=FailureDisposition.QUARANTINE,
                        )

                    if claim is not None and result.elapsed_seconds > min(claim.wall_seconds, budget_manager.policy.max_trial_wall_seconds):
                        result = WorkResult(
                            status=NodeStatus.TIMED_OUT,
                            metrics=result.metrics,
                            artifact_hashes=result.artifact_hashes,
                            elapsed_seconds=result.elapsed_seconds,
                            artifact_bytes=result.artifact_bytes,
                            failure_code="trial_wall_timeout",
                            failure_disposition=FailureDisposition.RETRYABLE,
                        )

                    if result.status in (NodeStatus.SUCCEEDED, NodeStatus.CACHED):
                        emit(node, SchedulerEventKind.COMPLETE, NodeStatus.RUNNING, result.status, attempt, worker_id, "work_completed", {"metrics": dict(result.metrics)})
                        append_ledger(node, LedgerAction.SUCCEEDED if result.status is NodeStatus.SUCCEEDED else LedgerAction.CACHED, "work_completed", result)
                        if claim is not None:
                            budget_manager.complete(result)
                        terminal = True
                    elif result.status is NodeStatus.PRUNED:
                        emit(node, SchedulerEventKind.COMPLETE, NodeStatus.RUNNING, NodeStatus.PRUNED, attempt, worker_id, "search_pruned")
                        append_ledger(node, LedgerAction.PRUNED, "search_pruned", result)
                        if claim is not None:
                            budget_manager.complete(result)
                        terminal = True
                    elif result.status is NodeStatus.CANCELLED:
                        emit(node, SchedulerEventKind.CANCEL, NodeStatus.RUNNING, NodeStatus.CANCELLED, attempt, worker_id, result.failure_code or "worker_cancelled")
                        append_ledger(node, LedgerAction.CANCELLED, result.failure_code or "worker_cancelled", result)
                        terminal = True
                    else:
                        retryable = result.failure_disposition is FailureDisposition.RETRYABLE
                        retry_available = attempt <= budget_manager.policy.max_retries
                        if retryable and retry_available:
                            emit(node, SchedulerEventKind.RETRY, NodeStatus.RUNNING, NodeStatus.READY, attempt, worker_id, result.failure_code)
                            append_ledger(node, LedgerAction.FAILED, f"retry:{result.failure_code}", result)
                            continue
                        after = NodeStatus.QUARANTINED if result.failure_disposition is FailureDisposition.QUARANTINE else result.status
                        kind = SchedulerEventKind.QUARANTINE if after is NodeStatus.QUARANTINED else (SchedulerEventKind.TIMEOUT if after is NodeStatus.TIMED_OUT else SchedulerEventKind.FAIL)
                        emit(node, kind, NodeStatus.RUNNING, after, attempt, worker_id, result.failure_code)
                        action = LedgerAction.TIMED_OUT if after is NodeStatus.TIMED_OUT else LedgerAction.FAILED
                        append_ledger(node, action, result.failure_code, result)
                        if claim is not None:
                            budget_manager.complete(result)
                        terminal = True
                pending.remove(node.node_id)

            if not progress and pending:
                unresolved = sorted(pending)
                raise ExperimentError(
                    "scheduler_deadlock",
                    "scheduler cannot make progress; DAG or state transition is invalid",
                    {"unresolved": unresolved},
                )

        blockers = tuple(
            f"node_terminal:{node_id}:{status.value}"
            for node_id, status in sorted(statuses.items())
            if status in terminal_failure
        )
        completed = not blockers
        event_stream_hash = canonical_sha256([asdict(event) for event in events])
        if not ledger.verify():
            raise ExperimentError("selection_ledger_chain_invalid", "selection ledger failed chain verification")
        return SchedulerRun(
            manifest_hash=manifest.manifest_hash,
            statuses=dict(statuses),
            attempts=dict(attempts),
            events=tuple(events),
            event_stream_hash=event_stream_hash,
            ledger_entries=ledger.entries,
            budget_usage=budget_manager.usage,
            completed=completed,
            blockers=blockers,
        )

    @staticmethod
    def _experiment_id(manifest: ExperimentManifest) -> str:
        trial_ids = manifest.trials
        if trial_ids:
            return trial_ids[0].experiment_id
        return manifest.manifest_id
