from __future__ import annotations

from typing import Any, Mapping, TypeVar

from .contracts import (
    ArtifactRef,
    ChaosReport,
    ChaosScenarioResult,
    CompileEvidence,
    CompileTargetResult,
    DifferentialCase,
    DifferentialReport,
    EnvironmentFingerprint,
    ProspectiveStageEvidence,
    QualificationPolicy,
    RecoveryReport,
    RollbackDrillReport,
    SecurityControlResult,
    SecurityReport,
    SoakReport,
)
from .enums import EvidenceStatus, ReleaseStage
from .errors import QualificationError

T = TypeVar("T")


def _require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise QualificationError("invalid_payload", f"{name} must be an object")
    return value


def parse_environment(data: Mapping[str, Any]) -> EnvironmentFingerprint:
    return EnvironmentFingerprint(**_require_mapping(data, "environment"))


def parse_policy(data: Mapping[str, Any]) -> QualificationPolicy:
    payload = dict(_require_mapping(data, "policy"))
    for key in ("required_compile_targets", "required_differential_cases", "required_chaos_scenarios", "required_security_controls"):
        payload[key] = tuple(payload[key])
    return QualificationPolicy(**payload)


def parse_compile(data: Mapping[str, Any]) -> CompileEvidence:
    payload = dict(_require_mapping(data, "compile evidence"))
    payload["targets"] = tuple(CompileTargetResult(**_require_mapping(item, "compile target")) for item in payload["targets"])
    payload["required_targets"] = tuple(payload["required_targets"])
    return CompileEvidence(**payload)


def parse_differential(data: Mapping[str, Any]) -> DifferentialReport:
    payload = dict(_require_mapping(data, "differential report"))
    payload["cases"] = tuple(DifferentialCase(**_require_mapping(item, "differential case")) for item in payload["cases"])
    payload["missing_case_ids"] = tuple(payload.get("missing_case_ids", ()))
    return DifferentialReport(**payload)


def parse_soak(data: Mapping[str, Any]) -> SoakReport:
    return SoakReport(**_require_mapping(data, "soak report"))


def parse_chaos(data: Mapping[str, Any]) -> ChaosReport:
    payload = dict(_require_mapping(data, "chaos report"))
    payload["scenarios"] = tuple(ChaosScenarioResult(**_require_mapping(item, "chaos scenario")) for item in payload["scenarios"])
    payload["required_scenario_ids"] = tuple(payload["required_scenario_ids"])
    return ChaosReport(**payload)


def parse_recovery(data: Mapping[str, Any]) -> RecoveryReport:
    return RecoveryReport(**_require_mapping(data, "recovery report"))


def parse_security(data: Mapping[str, Any]) -> SecurityReport:
    payload = dict(_require_mapping(data, "security report"))
    controls = []
    for item in payload["controls"]:
        control = dict(_require_mapping(item, "security control"))
        control["status"] = EvidenceStatus(control["status"])
        controls.append(SecurityControlResult(**control))
    payload["controls"] = tuple(controls)
    payload["required_control_ids"] = tuple(payload["required_control_ids"])
    return SecurityReport(**payload)


def parse_stage(data: Mapping[str, Any]) -> ProspectiveStageEvidence:
    payload = dict(_require_mapping(data, "prospective stage evidence"))
    payload["stage"] = ReleaseStage(payload["stage"])
    return ProspectiveStageEvidence(**payload)


def parse_rollback(data: Mapping[str, Any]) -> RollbackDrillReport:
    return RollbackDrillReport(**_require_mapping(data, "rollback report"))


def parse_artifact_refs(items: Any) -> tuple[ArtifactRef, ...]:
    if not isinstance(items, list):
        raise QualificationError("invalid_payload", "artifact_refs must be an array")
    return tuple(ArtifactRef(**_require_mapping(item, "artifact ref")) for item in items)
