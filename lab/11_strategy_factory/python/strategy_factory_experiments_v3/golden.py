"""Golden fixtures used by UCE-I11 tests, vectors, and diagnostics."""

from __future__ import annotations

from .canonical import canonical_sha256
from .contracts import (
    BudgetPolicy,
    CandidateAdmission,
    ExperimentDeclaration,
    ObjectiveSpec,
    ParameterSpec,
    SearchPlan,
    WorkResult,
)
from .enums import (
    AdmissionDecision,
    NodeStatus,
    ObjectiveDirection,
    ParameterKind,
    SearchKind,
)


def h(label: str) -> str:
    return canonical_sha256({"golden": label})


def golden_candidates() -> tuple[CandidateAdmission, ...]:
    return (
        CandidateAdmission(
            candidate_key="uce.classical.logistic",
            candidate_version="1.0.0",
            family="classical",
            trainer_key="uce.classical.logistic_ridge@1.0.0",
            decision=AdmissionDecision.ACCEPT,
            evidence_hash=h("classical-admission"),
            baseline=True,
            capability_flags={"deterministic": True, "exportable": True},
            estimated_memory_mb=128,
            estimated_wall_seconds=5.0,
        ),
        CandidateAdmission(
            candidate_key="uce.deep.temporal_conv",
            candidate_version="1.0.0",
            family="deep_sequence",
            trainer_key="uce.deep.causal_temporal_conv_ridge@1.0.0",
            decision=AdmissionDecision.WARN,
            evidence_hash=h("deep-admission"),
            warnings=("latency_margin_narrow",),
            capability_flags={"deterministic": True, "exportable": True, "known_time_audited": True},
            estimated_memory_mb=512,
            estimated_wall_seconds=10.0,
        ),
        CandidateAdmission(
            candidate_key="uce.deep.rejected_graph",
            candidate_version="1.0.0",
            family="deep_graph",
            trainer_key="uce.deep.graph@1.0.0",
            decision=AdmissionDecision.REJECT,
            evidence_hash=h("rejected-admission"),
            blockers=("future_perturbation_failed",),
            capability_flags={"deterministic": False},
            estimated_memory_mb=512,
            estimated_wall_seconds=10.0,
        ),
    )


def golden_search_plan(kind: SearchKind = SearchKind.QUASI_RANDOM, max_trials: int = 3) -> SearchPlan:
    return SearchPlan(
        search_id="uce_i11_golden_search",
        search_version="1.0.0",
        kind=kind,
        parameters=(
            ParameterSpec("alpha", ParameterKind.FLOAT, low=0.0001, high=0.1, log_scale=True),
            ParameterSpec("depth", ParameterKind.INTEGER, low=1, high=4, step=1),
            ParameterSpec("use_bias", ParameterKind.BOOLEAN, values=(False, True)),
            ParameterSpec("loss", ParameterKind.CATEGORICAL, values=("logloss", "brier")),
        ),
        max_trials=max_trials,
        seed=17,
        objectives=(
            ObjectiveSpec("validation_loss", ObjectiveDirection.MINIMIZE, 1.0),
            ObjectiveSpec("latency_ms", ObjectiveDirection.MINIMIZE, 0.05, constraint_max=25.0),
        ),
        baseline_parameters={"alpha": 0.01, "depth": 1, "use_bias": True, "loss": "logloss"},
        eta=3,
        min_resource=1,
        max_resource=9,
        warmup_trials=3,
    )


def golden_budget(max_trials: int = 12) -> BudgetPolicy:
    return BudgetPolicy(
        budget_id="uce_i11_golden_budget",
        budget_version="1.0.0",
        max_trials=max_trials,
        max_total_wall_seconds=300.0,
        max_trial_wall_seconds=30.0,
        max_memory_mb=2048,
        cpu_slots=2,
        gpu_slots=0,
        max_retries=1,
        max_artifact_bytes=256 * 1024 * 1024,
        max_seeds=2,
        max_folds=2,
        max_candidates=4,
        per_candidate_trial_cap=min(8, max_trials),
        retain_failed_artifacts=True,
        fail_closed=True,
    )


def golden_declaration(
    *,
    search_kind: SearchKind = SearchKind.QUASI_RANDOM,
    max_trials: int = 12,
    requested_roles: tuple[str, ...] = ("train", "validation"),
) -> ExperimentDeclaration:
    return ExperimentDeclaration(
        experiment_id="uce_i11_golden_experiment",
        experiment_version="1.0.0",
        dataset_id="dataset_context_v3",
        dataset_manifest_hash=h("dataset"),
        split_plan_id="walk_forward_v3",
        split_plan_hash=h("split"),
        transform_plan_hash=h("transform"),
        target_plan_hash=h("target"),
        economics_plan_hash=h("economics"),
        known_time_policy_hash=h("known-time"),
        candidates=golden_candidates(),
        folds=("wf_00", "wf_01"),
        seeds=(7, 19),
        search_plan=golden_search_plan(search_kind, max_trials=3),
        budget=golden_budget(max_trials=max_trials),
        scheduler_version="1.0.0",
        compiler_version="1.0.0",
        baseline_first=True,
        hidden_test_role="final_test",
        requested_roles=requested_roles,
        calibration_kinds=("none", "platt"),
        threshold_kinds=("default", "cost_optimal"),
        ensemble_kinds=("weighted_oof",),
        export_requested=True,
    )


def success_worker(node, attempt: int, worker_id: str) -> WorkResult:
    metric = int(node.payload_hash[:8], 16) / 0xFFFFFFFF
    return WorkResult(
        status=NodeStatus.SUCCEEDED,
        metrics={"score": metric},
        artifact_hashes=(canonical_sha256({"node": node.node_id, "attempt": attempt}),),
        elapsed_seconds=0.01,
        artifact_bytes=128,
    )
