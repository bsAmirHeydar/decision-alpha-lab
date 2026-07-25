"""Multi-seed, ablation, calibration, export, and latency qualification."""

from __future__ import annotations

from .canonical import canonical_sha256, stable_id
from .contracts import DeepQualificationReport
from .enums import AdmissionDecision, QualificationDecision
from .math_utils import mean, std


def qualify_deep_model(
    algorithm_key,
    dataset_manifest_hash,
    admission,
    seed_runs,
    ablations,
    export,
    baseline_metric,
    minimum_incremental_uplift=0.01,
    max_failed_run_rate=0.2,
    max_metric_std=0.05,
    max_latency_ms=5.0,
    max_calibration_error=0.1,
    maximize_metric=True,
):
    seed_runs = tuple(seed_runs)
    ablations = tuple(ablations)
    blockers = list(admission.blockers)
    warnings = list(admission.warnings)
    succeeded = tuple(run for run in seed_runs if run.status == "succeeded")
    failed_run_rate = 1.0 - len(succeeded) / max(1, len(seed_runs))
    metrics = [run.primary_metric for run in succeeded]
    utilities = [run.economic_utility for run in succeeded]
    mean_metric = mean(metrics)
    metric_std = std(metrics)
    mean_utility = mean(utilities)
    uplift = mean_metric - float(baseline_metric) if maximize_metric else float(baseline_metric) - mean_metric

    if admission.decision is AdmissionDecision.REJECT:
        blockers.append("deep_admission_rejected")
    if len(seed_runs) < 3:
        blockers.append("fewer_than_three_seed_runs")
    if len({run.seed for run in seed_runs}) != len(seed_runs):
        blockers.append("duplicate_seed_run")
    if not succeeded:
        blockers.append("no_successful_seed_run")
    if failed_run_rate > max_failed_run_rate:
        blockers.append("failed_run_rate_exceeded")
    if metric_std > max_metric_std:
        blockers.append("multi_seed_instability")
    if uplift < minimum_incremental_uplift:
        blockers.append("classical_incremental_uplift_failed")
    if mean_utility <= 0:
        blockers.append("non_positive_economic_utility")
    if not ablations:
        blockers.append("view_ablation_missing")
    elif not all(observation.passed for observation in ablations):
        blockers.append("view_ablation_failed")
    if not export.available:
        blockers.append("export_path_unavailable")
    if export.parity_max_abs_error > 1e-6:
        blockers.append("export_parity_failed")
    if export.latency_ms > max_latency_ms:
        blockers.append("latency_budget_exceeded")

    calibration_warning = any(run.calibration_error > max_calibration_error for run in succeeded)
    if blockers:
        decision = QualificationDecision.REJECTED
    elif calibration_warning:
        decision = QualificationDecision.CHALLENGER_ONLY
        warnings.append("calibration_requires_remediation")
    elif admission.decision is AdmissionDecision.WARN:
        decision = QualificationDecision.CHALLENGER_ONLY
        warnings.append("admission_warning_prevents_promotion")
    else:
        decision = QualificationDecision.PROMOTABLE

    blockers = list(dict.fromkeys(blockers))
    warnings = list(dict.fromkeys(warnings))
    material = {
        "algorithm_key": algorithm_key,
        "dataset_manifest_hash": dataset_manifest_hash,
        "admission_evidence_id": admission.evidence_id,
        "seed_runs": [run.artifact_hash for run in seed_runs],
        "ablations": [observation.evidence_hash for observation in ablations],
        "export": export.evidence_hash,
        "baseline_metric": float(baseline_metric),
        "mean_metric": mean_metric,
        "metric_std": metric_std,
        "mean_economic_utility": mean_utility,
        "failed_run_rate": failed_run_rate,
        "uplift": uplift,
        "minimum_incremental_uplift": float(minimum_incremental_uplift),
        "decision": decision.value,
        "blockers": blockers,
        "warnings": warnings,
    }
    return DeepQualificationReport(
        report_id=stable_id("ucequal", material),
        algorithm_key=algorithm_key,
        dataset_manifest_hash=dataset_manifest_hash,
        admission_evidence_id=admission.evidence_id,
        seed_runs=seed_runs,
        ablations=ablations,
        export=export,
        baseline_metric=float(baseline_metric),
        mean_metric=mean_metric,
        metric_std=metric_std,
        mean_economic_utility=mean_utility,
        failed_run_rate=failed_run_rate,
        minimum_incremental_uplift=float(minimum_incremental_uplift),
        decision=decision,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        evidence_hash=canonical_sha256(material),
    )
