from dataclasses import replace

from strategy_factory_experiments_v3.budget import BudgetManager
from strategy_factory_experiments_v3.compiler import ExperimentDagCompiler
from strategy_factory_experiments_v3.contracts import ResourceClaim, WorkResult
from strategy_factory_experiments_v3.enums import BudgetDecision, NodeStatus, ResourceDevice
from strategy_factory_experiments_v3.golden import golden_budget, golden_declaration


def claim(**overrides):
    values = dict(
        claim_id="claim_1",
        trial_id="trial_1",
        device=ResourceDevice.CPU,
        cpu_slots=1,
        gpu_slots=0,
        memory_mb=128,
        wall_seconds=5.0,
        artifact_bytes=1024,
        deterministic_required=True,
    )
    values.update(overrides)
    return ResourceClaim(**values)


def test_budget_allows_valid_claim_and_accounts_completion():
    manager = BudgetManager(golden_budget())
    assessment = manager.reserve(claim(), "candidate@1.0.0")
    assert assessment.decision is BudgetDecision.ALLOW
    manager.complete(WorkResult(NodeStatus.SUCCEEDED, elapsed_seconds=2.0, artifact_bytes=512))
    assert manager.usage.trials_started == 1
    assert manager.usage.trials_completed == 1
    assert manager.usage.total_wall_seconds == 2.0
    assert manager.usage.artifact_bytes == 512


def test_budget_denies_memory_cpu_gpu_and_trial_wall_overflow():
    policy = golden_budget()
    manager = BudgetManager(policy)
    assert manager.assess(claim(memory_mb=policy.max_memory_mb + 1), "c").decision is BudgetDecision.DENY
    assert manager.assess(claim(cpu_slots=policy.cpu_slots + 1), "c").decision is BudgetDecision.DENY
    assert manager.assess(claim(device=ResourceDevice.GPU, gpu_slots=1), "c").decision is BudgetDecision.DENY
    assert manager.assess(claim(wall_seconds=policy.max_trial_wall_seconds + 1), "c").decision is BudgetDecision.DENY


def test_per_candidate_trial_cap_is_hard():
    policy = replace(golden_budget(), per_candidate_trial_cap=1)
    manager = BudgetManager(policy)
    assert manager.reserve(claim(), "same").decision is BudgetDecision.ALLOW
    assert manager.reserve(replace(claim(), claim_id="claim_2", trial_id="trial_2"), "same").decision is BudgetDecision.DENY


def test_total_trial_count_is_hard():
    policy = replace(golden_budget(max_trials=1), per_candidate_trial_cap=1)
    manager = BudgetManager(policy)
    assert manager.reserve(claim(), "a").decision is BudgetDecision.ALLOW
    denial = manager.reserve(replace(claim(), claim_id="claim_2", trial_id="trial_2"), "b")
    assert denial.decision is BudgetDecision.DENY
    assert "trial_count_exhausted" in denial.reason_codes


def test_compiler_resource_claims_never_exceed_declared_budget():
    declaration = golden_declaration()
    manifest = ExperimentDagCompiler().compile(declaration)
    for item in manifest.resource_claims:
        assert item.memory_mb <= declaration.budget.max_memory_mb
        assert item.wall_seconds <= declaration.budget.max_trial_wall_seconds
        assert item.cpu_slots <= declaration.budget.cpu_slots
        assert item.gpu_slots <= declaration.budget.gpu_slots
