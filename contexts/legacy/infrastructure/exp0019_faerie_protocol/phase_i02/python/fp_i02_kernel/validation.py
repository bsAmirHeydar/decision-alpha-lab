"""Cross-contract validators and fail-closed health derivation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .config import ConfigurationBundle
from .contracts import ContextManifestRecord, DivergenceCandidate, HealthStatus, SymbolPair, WindowKey
from .enums import ContextProfile, ExecutionAuthority, HealthState, QuotaConsumptionPolicy, RelationCode
from .errors import FPI02Error
from .reason_codes import DEFAULT_REASON_REGISTRY
from .relations import DEFAULT_RELATION_REGISTRY


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    check_id: str
    passed: bool
    reason_code: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    subject: str
    findings: tuple[ValidationFinding, ...]

    @property
    def passed(self) -> bool:
        return all(item.passed for item in self.findings)

    @property
    def failure_codes(self) -> tuple[str, ...]:
        return tuple(item.reason_code for item in self.findings if not item.passed)


def validate_bundle(bundle: ConfigurationBundle) -> ValidationReport:
    findings: list[ValidationFinding] = []
    findings.append(ValidationFinding("FP-I02-CFG-001", bundle.semantic.relation_registry_version == DEFAULT_RELATION_REGISTRY.version, "FP_RC_INVALID_CONFIG", "relation registry version matches runtime"))
    findings.append(ValidationFinding("FP-I02-CFG-002", bundle.semantic.reason_registry_version == DEFAULT_REASON_REGISTRY.version, "FP_RC_INVALID_CONFIG", "reason registry version matches runtime"))
    findings.append(ValidationFinding("FP-I02-CFG-003", bundle.semantic.first_sweep_authority.value == "M1_ONLY", "FP_RC_INVALID_CONFIG", "first-sweep authority is M1 only"))
    findings.append(ValidationFinding("FP-I02-CFG-004", bundle.semantic.lookback_policy.value == "CALENDAR_DAY_DEPTH" and not bundle.semantic.replace_missing_offsets, "FP_RC_INVALID_CONFIG", "calendar offsets are not compressed"))
    findings.append(ValidationFinding("FP-I02-CFG-005", bundle.semantic.resolved_confirmation_timeframe_seconds > 0, "FP_RC_INVALID_CONFIG", "confirmation timeframe resolved at initialization"))
    live_allowed = not (bundle.profile is ContextProfile.CANONICAL_LIVE and bundle.semantic.quota_consumption_policy is QuotaConsumptionPolicy.UNSET)
    findings.append(ValidationFinding("FP-I02-CFG-006", live_allowed, "FP_RC_OPEN_DECISION_BLOCKS_LIVE", "open quota decision blocks live profile"))
    findings.append(ValidationFinding("FP-I02-CFG-007", bundle.execution_authority() is not ExecutionAuthority.LIVE, "FP_RC_LIVE_AUTHORITY_FORBIDDEN", "FP-I02 grants no live authority"))
    return ValidationReport("configuration_bundle", tuple(findings))


def validate_candidate_against_relation(candidate: DivergenceCandidate) -> ValidationReport:
    descriptor = DEFAULT_RELATION_REGISTRY.resolve(candidate.relation)
    findings = [
        ValidationFinding("FP-I02-CAND-001", candidate.hunter_symbol != candidate.protected_symbol, "FP_RC_SYMBOL_PAIR_INVALID", "roles are distinct"),
        ValidationFinding("FP-I02-CAND-002", descriptor.code is candidate.relation, "FP_RC_RELATION_DESCRIPTOR_INVALID", "candidate relation exists"),
        ValidationFinding("FP-I02-CAND-003", candidate.first_hunt_m1_utc_ms % 60000 == 0, "FP_RC_INVALID_CONFIG", "first hunt is M1 aligned"),
        ValidationFinding("FP-I02-CAND-004", candidate.confirmation_deadline_utc_ms > candidate.first_hunt_m1_utc_ms, "FP_RC_INVALID_CONFIG", "deadline follows hunt"),
    ]
    return ValidationReport(candidate.candidate_id, tuple(findings))


def validate_manifest(manifest: ContextManifestRecord) -> ValidationReport:
    findings = [
        ValidationFinding("FP-I02-MAN-001", manifest.context_id == "FP-CONTEXT-001", "FP_RC_INVALID_CONFIG", "context ID is canonical"),
        ValidationFinding("FP-I02-MAN-002", manifest.execution_authority is not ExecutionAuthority.LIVE, "FP_RC_LIVE_AUTHORITY_FORBIDDEN", "phase authority is not live"),
        ValidationFinding("FP-I02-MAN-003", manifest.relation_registry_hash == DEFAULT_RELATION_REGISTRY.registry_hash, "FP_RC_INVALID_CONFIG", "relation hash matches"),
        ValidationFinding("FP-I02-MAN-004", manifest.reason_registry_hash == DEFAULT_REASON_REGISTRY.registry_hash, "FP_RC_INVALID_CONFIG", "reason hash matches"),
    ]
    return ValidationReport(manifest.context_epoch_id, tuple(findings))


def derive_health(
    semantic_config_hash: str,
    dependency_snapshot_hash: str,
    reports: Iterable[ValidationReport],
    checked_utc_ms: int,
) -> HealthStatus:
    failures = [finding for report in reports for finding in report.findings if not finding.passed]
    codes = tuple(dict.fromkeys(finding.reason_code for finding in failures))
    if any(DEFAULT_REASON_REGISTRY.resolve(code).severity.value in {"ERROR", "CRITICAL"} for code in codes):
        state = HealthState.BLOCKED
    elif codes:
        state = HealthState.DEGRADED
    else:
        state = HealthState.READY
        codes = ("FP_RC_READY",)
    return HealthStatus(state, codes[0], codes, checked_utc_ms, semantic_config_hash, dependency_snapshot_hash)
