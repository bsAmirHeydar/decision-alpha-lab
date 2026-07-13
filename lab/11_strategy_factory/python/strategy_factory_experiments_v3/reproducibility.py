"""Manifest, event-stream, and artifact reproducibility auditing."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Mapping, Sequence

from .canonical import canonical_sha256, stable_id
from .compiler import manifest_semantic_snapshot
from .contracts import ArtifactComparison, ExperimentManifest, ReproducibilityReport


def compare_numeric_artifact(
    name: str,
    expected_values: Sequence[float],
    actual_values: Sequence[float],
    tolerance: float,
) -> ArtifactComparison:
    expected_hash = canonical_sha256(tuple(expected_values))
    actual_hash = canonical_sha256(tuple(actual_values))
    if len(expected_values) != len(actual_values):
        return ArtifactComparison(name, expected_hash, actual_hash, False, 1e308, tolerance)
    max_error = max((abs(float(left) - float(right)) for left, right in zip(expected_values, actual_values)), default=0.0)
    return ArtifactComparison(name, expected_hash, actual_hash, max_error <= tolerance, max_error, tolerance)


def audit_reproducibility(
    *,
    manifest: ExperimentManifest,
    rerun_manifest: ExperimentManifest,
    executed_trial_ids: Iterable[str],
    selected_trial_ids_expected: Iterable[str],
    selected_trial_ids_actual: Iterable[str],
    artifact_comparisons: Sequence[ArtifactComparison],
    event_stream_hash_expected: str,
    event_stream_hash_actual: str,
) -> ReproducibilityReport:
    blockers: list[str] = []
    warnings: list[str] = []
    original_semantics = canonical_sha256(manifest_semantic_snapshot(manifest))
    rerun_semantics = canonical_sha256(manifest_semantic_snapshot(rerun_manifest))
    if original_semantics != rerun_semantics:
        blockers.append("manifest_semantics_changed")
    executed = tuple(executed_trial_ids)
    if len(executed) != manifest.declared_trial_count:
        blockers.append("declared_executed_trial_count_mismatch")
    if len(set(executed)) != len(executed):
        blockers.append("duplicate_executed_trial_id")
    expected_selected = tuple(sorted(selected_trial_ids_expected))
    actual_selected = tuple(sorted(selected_trial_ids_actual))
    if expected_selected != actual_selected:
        blockers.append("selected_trial_set_changed")
    if event_stream_hash_expected != event_stream_hash_actual:
        blockers.append("event_stream_changed")
    for comparison in artifact_comparisons:
        if not comparison.within_tolerance:
            blockers.append(f"artifact_outside_tolerance:{comparison.artifact_name}")
        elif comparison.expected_hash != comparison.actual_hash:
            warnings.append(f"artifact_numeric_tolerance_used:{comparison.artifact_name}")
    passed = not blockers
    body = {
        "manifest_hash": manifest.manifest_hash,
        "rerun_manifest_hash": rerun_manifest.manifest_hash,
        "declared_trial_count": manifest.declared_trial_count,
        "executed_trial_count": len(executed),
        "selected_trial_ids_expected": expected_selected,
        "selected_trial_ids_actual": actual_selected,
        "artifact_comparisons": [asdict(item) for item in artifact_comparisons],
        "event_stream_hash_expected": event_stream_hash_expected,
        "event_stream_hash_actual": event_stream_hash_actual,
        "passed": passed,
        "blockers": blockers,
        "warnings": warnings,
    }
    return ReproducibilityReport(
        report_id=stable_id("ucerepro", body),
        manifest_hash=manifest.manifest_hash,
        rerun_manifest_hash=rerun_manifest.manifest_hash,
        declared_trial_count=manifest.declared_trial_count,
        executed_trial_count=len(executed),
        selected_trial_ids_expected=expected_selected,
        selected_trial_ids_actual=actual_selected,
        artifact_comparisons=tuple(artifact_comparisons),
        event_stream_hash_expected=event_stream_hash_expected,
        event_stream_hash_actual=event_stream_hash_actual,
        passed=passed,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        report_hash=canonical_sha256(body),
    )
