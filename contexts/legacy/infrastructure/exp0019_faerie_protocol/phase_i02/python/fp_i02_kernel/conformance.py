"""Executable conformance suite for FP-I02 public contracts."""
from __future__ import annotations

from dataclasses import replace

from .config import ProjectionConfiguration, canonical_research_bundle
from .enums import CandidateState, QuotaConsumptionPolicy, QuotaState, ReferenceState, WWState
from .errors import FPI02Error
from .golden import golden_bundle, golden_candidate, golden_manifest, golden_signal, golden_vector_material
from .identity import IdentityLedger, candidate_identity, projection_identity, signal_identity
from .lifecycle import CANDIDATE_MACHINE, QUOTA_MACHINE, REFERENCE_MACHINE, WW_MACHINE
from .reason_codes import DEFAULT_REASON_REGISTRY
from .registry import DEFAULT_CONTRACT_REGISTRY
from .relations import DEFAULT_RELATION_REGISTRY
from .validation import validate_bundle, validate_manifest


def run_conformance() -> dict:
    checks: list[dict] = []

    def check(check_id: str, passed: bool, evidence: str = "") -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    bundle = golden_bundle()
    manifest = golden_manifest()
    candidate = golden_candidate()
    signal = golden_signal()

    check("FP-I02-CONF-001", golden_vector_material() == golden_vector_material(), "golden vectors repeat exactly")
    check("FP-I02-CONF-002", validate_bundle(bundle).passed, "canonical research bundle passes")
    check("FP-I02-CONF-003", validate_manifest(manifest).passed, "manifest passes")
    check("FP-I02-CONF-004", len(DEFAULT_RELATION_REGISTRY.all()) == 7, "seven relations")
    check("FP-I02-CONF-005", len(DEFAULT_REASON_REGISTRY.all()) == 35, "closed reason registry")
    check("FP-I02-CONF-006", len(DEFAULT_CONTRACT_REGISTRY.all()) == 16, "public contract registry")

    style_change = replace(bundle.projection, line_width=2, active_opacity=240)
    changed_bundle = replace(bundle, projection=style_change)
    check("FP-I02-CONF-007", changed_bundle.semantic.config_hash == bundle.semantic.config_hash, "style does not change semantic hash")
    check("FP-I02-CONF-008", changed_bundle.projection.config_hash != bundle.projection.config_hash, "style changes projection hash")
    changed_semantic = replace(bundle.semantic, historical_n_depth=bundle.semantic.historical_n_depth + 1)
    check("FP-I02-CONF-009", changed_semantic.config_hash != bundle.semantic.config_hash, "behavior field changes semantic hash")

    same_signal = replace(signal, eligibility=signal.eligibility, reason_code="FP_RC_SUPPRESSED_BY_WW")
    check("FP-I02-CONF-010", signal_identity(signal).compact_id == signal_identity(same_signal).compact_id, "policy child state does not mutate signal identity")
    changed_signal = replace(signal, semantic_config_hash=changed_semantic.config_hash)
    check("FP-I02-CONF-011", signal_identity(signal).compact_id != signal_identity(changed_signal).compact_id, "semantic config changes signal ID")

    projection_a = projection_identity(signal.signal_id, bundle.projection.config_hash, "SIGNAL_LINE", "CHART-1")
    projection_b = projection_identity(signal.signal_id, changed_bundle.projection.config_hash, "SIGNAL_LINE", "CHART-1")
    check("FP-I02-CONF-012", projection_a.compact_id != projection_b.compact_id, "projection style changes object identity")

    ledger = IdentityLedger()
    check("FP-I02-CONF-013", ledger.register(candidate_identity(candidate)) == "REGISTERED", "first identity registered")
    check("FP-I02-CONF-014", ledger.register(candidate_identity(candidate)) == "DUPLICATE", "exact duplicate deduped")

    check("FP-I02-CONF-015", CANDIDATE_MACHINE.can_transition(CandidateState.OBSERVED, CandidateState.RAW_CANDIDATE), "candidate legal transition")
    check("FP-I02-CONF-016", not CANDIDATE_MACHINE.can_transition(CandidateState.CONFIRMED, CandidateState.RAW_CANDIDATE), "candidate terminal state")
    check("FP-I02-CONF-017", REFERENCE_MACHINE.can_transition(ReferenceState.HUNTER_SEEN, ReferenceState.CONSUMED_BY_PROTECTED_TOUCH), "reference reuse lifecycle")
    check("FP-I02-CONF-018", WW_MACHINE.can_transition(WWState.CONFIRMED, WWState.NEUTRALIZED), "WW neutralization")
    try:
        QUOTA_MACHINE.transition("q", QuotaState.RESERVED, QuotaState.CONSUMED, "evt", 1, "FP_RC_READY", QuotaConsumptionPolicy.UNSET)
        quota_blocked = False
    except FPI02Error as exc:
        quota_blocked = exc.code == "FP_RC_OPEN_DECISION_BLOCKS_LIVE"
    check("FP-I02-CONF-019", quota_blocked, "open Q12 blocks consumption")

    passed = all(item["passed"] for item in checks)
    return {
        "phase": "FP-I02",
        "version": "1.0.0",
        "passed": passed,
        "check_count": len(checks),
        "checks": checks,
        "golden": golden_vector_material(),
        "relation_registry_hash": DEFAULT_RELATION_REGISTRY.registry_hash,
        "reason_registry_hash": DEFAULT_REASON_REGISTRY.registry_hash,
        "contract_registry_hash": DEFAULT_CONTRACT_REGISTRY.registry_hash,
    }
