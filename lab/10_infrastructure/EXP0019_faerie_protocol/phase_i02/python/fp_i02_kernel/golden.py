"""Deterministic golden objects for FP-I02 tests and cross-language vectors."""
from __future__ import annotations

from .canonical import canonical_sha256
from .config import ConfigurationBundle, ProjectionConfiguration, canonical_research_bundle
from .contracts import (
    ConfirmationEvent,
    ConfirmedSignal,
    DivergenceCandidate,
    HuntFact,
    QuotaKey,
    ReasonEvidence,
    ReferenceSideKey,
    SymbolPair,
    WindowKey,
    WWContextRecord,
)
from .enums import (
    CandidateState,
    Direction,
    EligibilityState,
    PriceSide,
    RelationCode,
    SymbolRole,
    WWState,
    WindowKind,
    WindowScope,
)


def golden_bundle() -> ConfigurationBundle:
    return canonical_research_bundle(adapter_snapshot_hash="a" * 64)


def golden_manifest():
    return golden_bundle().build_manifest(1_782_000_000_000)


def golden_window_key() -> WindowKey:
    manifest = golden_manifest()
    return WindowKey(
        context_id="FP-CONTEXT-001",
        pair_id=manifest.pair.pair_id,
        kind=WindowKind.A,
        scope=WindowScope.SAME_TRADING_DAY,
        trading_day_id="NYDAY-2026-07-13",
        start_utc_ms=1_783_900_800_000,
        end_utc_ms=1_783_936_800_000,
        timezone="America/New_York",
        data_revision="FIXTURE-DATA-REV-001",
    )


def golden_reference_key() -> ReferenceSideKey:
    return ReferenceSideKey(golden_window_key().window_id, "NDXUSD", PriceSide.HIGH, 22500.25, "FIXTURE-DATA-REV-001")


def golden_hunt() -> HuntFact:
    manifest = golden_manifest()
    reference = golden_reference_key()
    return HuntFact(
        context_epoch_id=manifest.context_epoch_id,
        relation=RelationCode.AL,
        reference_side_id=reference.reference_side_id,
        check_window_id="FPWIN_CHECK_L_20260713",
        pair_id=manifest.pair.pair_id,
        symbol="NDXUSD",
        role=SymbolRole.HUNTER,
        side=PriceSide.HIGH,
        m1_open_utc_ms=1_783_944_000_000,
        observed_price=22500.50,
        reference_price=22500.25,
        data_revision="FIXTURE-DATA-REV-001",
        source_fingerprint="b" * 64,
    )


def golden_candidate() -> DivergenceCandidate:
    manifest = golden_manifest()
    hunt = golden_hunt()
    return DivergenceCandidate(
        context_epoch_id=manifest.context_epoch_id,
        relation=RelationCode.AL,
        direction=Direction.BEARISH,
        pair_id=manifest.pair.pair_id,
        hunter_symbol="NDXUSD",
        protected_symbol="SPXUSD",
        reference_window_id=golden_window_key().window_id,
        check_window_id=hunt.check_window_id,
        reference_side=PriceSide.HIGH,
        hunter_hunt_id=hunt.hunt_id,
        first_hunt_m1_utc_ms=hunt.m1_open_utc_ms,
        confirmation_deadline_utc_ms=1_783_963_800_000,
        resolved_confirmation_timeframe_seconds=3600,
        calendar_offset=0,
        state=CandidateState.RAW_CANDIDATE,
        data_revision="FIXTURE-DATA-REV-001",
        reason_code="FP_RC_READY",
    )


def golden_confirmation() -> ConfirmationEvent:
    candidate = golden_candidate()
    return ConfirmationEvent(
        candidate_id=candidate.candidate_id,
        confirmation_bar_open_utc_ms=1_783_944_000_000,
        confirmation_bar_close_utc_ms=1_783_947_600_000,
        confirmation_price=6230.50,
        state=CandidateState.CONFIRMED,
        reason_code="FP_RC_CONFIRMED_ACTIVE",
        data_revision="FIXTURE-DATA-REV-001",
    )


def golden_signal() -> ConfirmedSignal:
    candidate = golden_candidate()
    confirmation = golden_confirmation()
    return ConfirmedSignal(
        candidate_id=candidate.candidate_id,
        confirmation_event_id=confirmation.confirmation_event_id,
        relation=candidate.relation,
        direction=candidate.direction,
        pair_id=candidate.pair_id,
        hunter_symbol=candidate.hunter_symbol,
        protected_symbol=candidate.protected_symbol,
        first_hunt_m1_utc_ms=candidate.first_hunt_m1_utc_ms,
        confirmed_utc_ms=confirmation.confirmation_bar_close_utc_ms,
        eligibility=EligibilityState.ELIGIBLE,
        reason_code="FP_RC_CONFIRMED_ACTIVE",
        semantic_config_hash=golden_bundle().semantic.config_hash,
    )


def golden_ww() -> WWContextRecord:
    return WWContextRecord(
        signal_id="FPSIG_WW_FIXTURE_001",
        direction=Direction.BULLISH,
        state=WWState.CONFIRMED,
        confirmed_utc_ms=1_783_800_000_000,
    )


def golden_quota_key() -> QuotaKey:
    return QuotaKey(golden_manifest().context_epoch_id, "NYDAY-2026-07-13", golden_manifest().pair.pair_id, WindowKind.L)


def golden_reason_evidence() -> ReasonEvidence:
    signal = golden_signal()
    return ReasonEvidence("FP_RC_CONFIRMED_ACTIVE", signal.signal_id, signal.confirmed_utc_ms, {"relation": signal.relation.value})


def golden_vector_material() -> dict:
    bundle = golden_bundle()
    manifest = golden_manifest()
    window = golden_window_key()
    reference = golden_reference_key()
    hunt = golden_hunt()
    candidate = golden_candidate()
    confirmation = golden_confirmation()
    signal = golden_signal()
    quota = golden_quota_key()
    return {
        "semantic_config_hash": bundle.semantic.config_hash,
        "projection_config_hash": bundle.projection.config_hash,
        "context_epoch_id": manifest.context_epoch_id,
        "manifest_hash": manifest.manifest_hash,
        "pair_id": manifest.pair.pair_id,
        "window_id": window.window_id,
        "reference_side_id": reference.reference_side_id,
        "hunt_id": hunt.hunt_id,
        "candidate_id": candidate.candidate_id,
        "confirmation_event_id": confirmation.confirmation_event_id,
        "signal_id": signal.signal_id,
        "quota_key_id": quota.quota_key_id,
        "reason_evidence_id": golden_reason_evidence().evidence_id,
        "vector_hash": canonical_sha256({
            "manifest": manifest,
            "window": window,
            "reference": reference,
            "hunt": hunt,
            "candidate": candidate,
            "confirmation": confirmation,
            "signal": signal,
            "quota": quota,
        }),
    }
