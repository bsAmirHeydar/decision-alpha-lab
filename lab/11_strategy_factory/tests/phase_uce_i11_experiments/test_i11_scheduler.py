from collections import defaultdict

from strategy_factory_experiments_v3.budget import BudgetManager
from strategy_factory_experiments_v3.compiler import ExperimentDagCompiler
from strategy_factory_experiments_v3.contracts import WorkResult
from strategy_factory_experiments_v3.enums import FailureDisposition, NodeKind, NodeStatus, SchedulerEventKind
from strategy_factory_experiments_v3.golden import golden_declaration, success_worker
from strategy_factory_experiments_v3.scheduler import DeterministicScheduler


def build():
    declaration = golden_declaration(max_trials=4)
    manifest = ExperimentDagCompiler().compile(declaration)
    return declaration, manifest


def test_scheduler_replays_identical_event_stream():
    declaration, manifest = build()
    first = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), success_worker)
    second = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), success_worker)
    assert first.completed and second.completed
    assert first.event_stream_hash == second.event_stream_hash
    assert first.events == second.events
    assert first.statuses == second.statuses


def test_scheduler_retries_retryable_failure_once_then_succeeds():
    declaration, manifest = build()
    target = next(node.node_id for node in manifest.nodes if node.kind is NodeKind.TRIAL)

    def worker(node, attempt, worker_id):
        if node.node_id == target and attempt == 1:
            return WorkResult(
                NodeStatus.FAILED,
                elapsed_seconds=0.01,
                failure_code="transient_io",
                failure_disposition=FailureDisposition.RETRYABLE,
            )
        return success_worker(node, attempt, worker_id)

    run = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), worker)
    assert run.statuses[target] is NodeStatus.SUCCEEDED
    assert run.attempts[target] == 2
    assert any(event.kind is SchedulerEventKind.RETRY and event.node_id == target for event in run.events)


def test_scheduler_quarantines_unexpected_worker_exception_and_skips_descendants():
    declaration, manifest = build()
    target = next(node.node_id for node in manifest.nodes if node.kind is NodeKind.TRIAL)

    def worker(node, attempt, worker_id):
        if node.node_id == target:
            raise RuntimeError("boom")
        return success_worker(node, attempt, worker_id)

    run = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), worker)
    assert run.statuses[target] is NodeStatus.QUARANTINED
    descendants = [node for node in manifest.nodes if target in node.dependencies]
    assert descendants
    assert all(run.statuses[node.node_id] is NodeStatus.SKIPPED for node in descendants)
    assert not run.completed


def test_scheduler_cancellation_is_evidence_and_cascades():
    declaration, manifest = build()
    target = next(node.node_id for node in manifest.nodes if node.kind is NodeKind.TRIAL)
    run = DeterministicScheduler().run(
        manifest,
        BudgetManager(declaration.budget),
        success_worker,
        cancelled_node_ids=frozenset({target}),
    )
    assert run.statuses[target] is NodeStatus.CANCELLED
    assert any(event.kind is SchedulerEventKind.CANCEL for event in run.events if event.node_id == target)
    assert not run.completed


def test_scheduler_enforces_trial_timeout_after_worker_result():
    declaration, manifest = build()
    target = next(node.node_id for node in manifest.nodes if node.kind is NodeKind.TRIAL)

    def worker(node, attempt, worker_id):
        if node.node_id == target:
            return WorkResult(
                NodeStatus.SUCCEEDED,
                elapsed_seconds=999.0,
                failure_disposition=FailureDisposition.RETRYABLE,
            )
        return success_worker(node, attempt, worker_id)

    run = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), worker)
    assert run.statuses[target] is NodeStatus.TIMED_OUT
    assert run.attempts[target] == declaration.budget.max_retries + 1
    assert not run.completed


def test_valid_cache_resolver_skips_worker_and_marks_cached():
    declaration, manifest = build()
    target = next(node.node_id for node in manifest.nodes if node.kind is NodeKind.TRANSFORM)
    calls = defaultdict(int)

    def worker(node, attempt, worker_id):
        calls[node.node_id] += 1
        return success_worker(node, attempt, worker_id)

    def cache_resolver(node):
        if node.node_id == target:
            return WorkResult(NodeStatus.CACHED, artifact_hashes=("a" * 64,))
        return None

    run = DeterministicScheduler().run(
        manifest,
        BudgetManager(declaration.budget),
        worker,
        cache_resolver=cache_resolver,
    )
    assert run.statuses[target] is NodeStatus.CACHED
    assert calls[target] == 0
    assert run.completed


def test_worker_ids_are_attempt_scoped_and_unique():
    declaration, manifest = build()
    run = DeterministicScheduler().run(manifest, BudgetManager(declaration.budget), success_worker)
    starts = [event for event in run.events if event.kind is SchedulerEventKind.START]
    assert len({event.worker_id for event in starts}) == len(starts)
    assert all(event.worker_id.startswith("uceworker_") for event in starts)


def test_scheduler_resumes_validated_success_prefix_without_reexecution():
    declaration, manifest = build()
    dataset = next(node for node in manifest.nodes if node.kind is NodeKind.DATASET)
    calls = defaultdict(int)

    def worker(node, attempt, worker_id):
        calls[node.node_id] += 1
        return success_worker(node, attempt, worker_id)

    run = DeterministicScheduler().run(
        manifest,
        BudgetManager(declaration.budget),
        worker,
        resume_statuses={dataset.node_id: NodeStatus.SUCCEEDED},
    )
    assert run.completed
    assert calls[dataset.node_id] == 0
    assert any(event.kind is SchedulerEventKind.RESUME and event.node_id == dataset.node_id for event in run.events)
