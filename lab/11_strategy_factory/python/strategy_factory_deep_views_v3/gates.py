"""Admission gates that prevent premature deep-model experimentation."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import canonical_sha256, stable_id
from .contracts import DeepAdmissionEvidence
from .enums import AdmissionDecision
from .errors import DeepViewError


@dataclass(frozen=True, slots=True)
class DeepAdmissionThresholds:
    minimum_effective_sample_size: float = 500.0
    minimum_clusters: int = 50
    minimum_event_diversity: int = 3
    warning_sample_multiplier: float = 2.0

    def __post_init__(self) -> None:
        if self.minimum_effective_sample_size <= 0:
            raise DeepViewError("invalid_admission_threshold", "minimum effective sample size must be positive")
        if self.minimum_clusters < 1 or self.minimum_event_diversity < 1:
            raise DeepViewError("invalid_admission_threshold", "cluster and event-diversity thresholds must be positive")
        if self.warning_sample_multiplier < 1.0:
            raise DeepViewError("invalid_admission_threshold", "warning multiplier must be at least one")


def evaluate_deep_admission(
    dataset_id: str,
    dataset_manifest_hash: str,
    effective_sample_size: float,
    dependence_cluster_count: int,
    event_diversity_count: int,
    stable_dimensions: bool,
    known_time_audit_passed: bool,
    future_perturbation_passed: bool,
    classical_gate_passed: bool,
    classical_best_metric: float,
    augmentation_policy_hash: str,
    ablation_plan_hash: str,
    minimum_effective_sample_size: float = 500,
    minimum_clusters: int = 50,
    minimum_event_diversity: int = 3,
) -> DeepAdmissionEvidence:
    thresholds = DeepAdmissionThresholds(
        float(minimum_effective_sample_size),
        int(minimum_clusters),
        int(minimum_event_diversity),
    )
    blockers: list[str] = []
    warnings: list[str] = []
    if not dataset_id:
        blockers.append("dataset_id_missing")
    if not dataset_manifest_hash:
        blockers.append("dataset_manifest_hash_missing")
    if effective_sample_size < thresholds.minimum_effective_sample_size:
        blockers.append("insufficient_effective_sample_size")
    if dependence_cluster_count < thresholds.minimum_clusters:
        blockers.append("insufficient_dependence_clusters")
    if event_diversity_count < thresholds.minimum_event_diversity:
        blockers.append("insufficient_event_diversity")
    if not stable_dimensions:
        blockers.append("unstable_representation_dimensions")
    if not known_time_audit_passed:
        blockers.append("known_time_audit_failed")
    if not future_perturbation_passed:
        blockers.append("future_perturbation_failed")
    if not classical_gate_passed:
        blockers.append("classical_gate_failed")
    if not augmentation_policy_hash:
        blockers.append("augmentation_policy_missing")
    if not ablation_plan_hash:
        blockers.append("ablation_plan_missing")

    if not blockers:
        if effective_sample_size < thresholds.warning_sample_multiplier * thresholds.minimum_effective_sample_size:
            warnings.append("sample_size_near_minimum")
        if dependence_cluster_count < 2 * thresholds.minimum_clusters:
            warnings.append("dependence_cluster_count_near_minimum")
        if event_diversity_count == thresholds.minimum_event_diversity:
            warnings.append("event_diversity_at_minimum")

    decision = (
        AdmissionDecision.REJECT
        if blockers
        else AdmissionDecision.WARN
        if warnings
        else AdmissionDecision.ACCEPT
    )
    material = {
        "dataset_id": dataset_id,
        "dataset_manifest_hash": dataset_manifest_hash,
        "effective_sample_size": float(effective_sample_size),
        "dependence_cluster_count": int(dependence_cluster_count),
        "event_diversity_count": int(event_diversity_count),
        "stable_dimensions": bool(stable_dimensions),
        "known_time_audit_passed": bool(known_time_audit_passed),
        "future_perturbation_passed": bool(future_perturbation_passed),
        "classical_gate_passed": bool(classical_gate_passed),
        "classical_best_metric": float(classical_best_metric),
        "augmentation_policy_hash": augmentation_policy_hash,
        "ablation_plan_hash": ablation_plan_hash,
        "thresholds": thresholds,
        "decision": decision.value,
        "blockers": blockers,
        "warnings": warnings,
    }
    return DeepAdmissionEvidence(
        evidence_id=stable_id("uceadmission", material),
        dataset_id=dataset_id or "missing",
        dataset_manifest_hash=dataset_manifest_hash,
        effective_sample_size=float(effective_sample_size),
        dependence_cluster_count=int(dependence_cluster_count),
        event_diversity_count=int(event_diversity_count),
        stable_dimensions=bool(stable_dimensions),
        known_time_audit_passed=bool(known_time_audit_passed),
        future_perturbation_passed=bool(future_perturbation_passed),
        classical_gate_passed=bool(classical_gate_passed),
        classical_best_metric=float(classical_best_metric),
        augmentation_policy_hash=augmentation_policy_hash,
        ablation_plan_hash=ablation_plan_hash,
        decision=decision,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        evidence_hash=canonical_sha256(material),
    )
