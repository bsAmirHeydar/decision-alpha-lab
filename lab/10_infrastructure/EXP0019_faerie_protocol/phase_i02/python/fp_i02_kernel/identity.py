"""Canonical semantic and projection identity builders."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .canonical import canonical_sha256, projection_hash, semantic_hash, stable_id
from .contracts import (
    ConfirmationEvent,
    ConfirmedSignal,
    DivergenceCandidate,
    HuntFact,
    QuotaKey,
    ReferenceSideKey,
    WindowKey,
    WWContextRecord,
)
from .errors import FPI02Error


@dataclass(frozen=True, slots=True)
class IdentityEnvelope:
    identity_domain: str
    object_type: str
    schema_version: str
    semantic_hash: str
    compact_id: str
    payload_hash: str


PREFIX_BY_TYPE = {
    "context_epoch": "FPEPOCH",
    "window": "FPWIN",
    "reference_side": "FPREF",
    "hunt": "FPHUNT",
    "candidate": "FPCAND",
    "confirmation": "FPCONF",
    "signal": "FPSIG",
    "ww_context": "FPWW",
    "quota_key": "FPQUOTA",
    "projection": "FPPROJ",
    "reason_evidence": "FPREASON",
}


def build_identity(object_type: str, payload: Any, schema_version: str = "1.0.0", domain: str = "SEMANTIC") -> IdentityEnvelope:
    if object_type not in PREFIX_BY_TYPE:
        raise FPI02Error("FP_RC_INVALID_IDENTIFIER", f"unsupported identity object type: {object_type}")
    if domain not in {"SEMANTIC", "PROJECTION"}:
        raise FPI02Error("FP_RC_INVALID_IDENTIFIER", "identity domain must be SEMANTIC or PROJECTION")
    # Public semantic object IDs match the contract-level canonical payload hash.
    # The object-type prefix supplies domain separation; projection IDs retain an
    # explicit projection-domain wrapper because multiple chart objects may be
    # derived from one semantic signal.
    digest = canonical_sha256(payload) if domain == "SEMANTIC" else projection_hash(payload)
    compact = f"{PREFIX_BY_TYPE[object_type]}_{digest[:32]}"
    return IdentityEnvelope(domain, object_type, schema_version, digest, compact, canonical_sha256(payload))


def window_identity(value: WindowKey) -> IdentityEnvelope:
    return build_identity("window", value)


def reference_identity(value: ReferenceSideKey) -> IdentityEnvelope:
    return build_identity("reference_side", value)


def hunt_identity(value: HuntFact) -> IdentityEnvelope:
    return build_identity("hunt", value)


def candidate_identity(value: DivergenceCandidate) -> IdentityEnvelope:
    # Candidate state/reason are deliberately excluded because identity describes the economic setup.
    payload = {
        "context_epoch_id": value.context_epoch_id,
        "relation": value.relation,
        "direction": value.direction,
        "pair_id": value.pair_id,
        "hunter_symbol": value.hunter_symbol,
        "protected_symbol": value.protected_symbol,
        "reference_window_id": value.reference_window_id,
        "check_window_id": value.check_window_id,
        "reference_side": value.reference_side,
        "first_hunt_m1_utc_ms": value.first_hunt_m1_utc_ms,
        "confirmation_deadline_utc_ms": value.confirmation_deadline_utc_ms,
        "resolved_confirmation_timeframe_seconds": value.resolved_confirmation_timeframe_seconds,
        "calendar_offset": value.calendar_offset,
        "data_revision": value.data_revision,
        "candidate_version": value.candidate_version,
    }
    return build_identity("candidate", payload)


def confirmation_identity(value: ConfirmationEvent) -> IdentityEnvelope:
    return build_identity("confirmation", value)


def signal_identity(value: ConfirmedSignal) -> IdentityEnvelope:
    payload = {
        "candidate_id": value.candidate_id,
        "confirmation_event_id": value.confirmation_event_id,
        "relation": value.relation,
        "direction": value.direction,
        "pair_id": value.pair_id,
        "hunter_symbol": value.hunter_symbol,
        "protected_symbol": value.protected_symbol,
        "first_hunt_m1_utc_ms": value.first_hunt_m1_utc_ms,
        "confirmed_utc_ms": value.confirmed_utc_ms,
        "semantic_config_hash": value.semantic_config_hash,
        "signal_version": value.signal_version,
    }
    return build_identity("signal", payload)


def ww_identity(value: WWContextRecord) -> IdentityEnvelope:
    return build_identity("ww_context", value)


def quota_identity(value: QuotaKey) -> IdentityEnvelope:
    return build_identity("quota_key", value)


def projection_identity(signal_id: str, projection_config_hash: str, object_role: str, chart_instance_id: str) -> IdentityEnvelope:
    if not signal_id or not projection_config_hash or not object_role or not chart_instance_id:
        raise FPI02Error("FP_RC_INVALID_IDENTIFIER", "projection identity fields are required")
    return build_identity(
        "projection",
        {
            "signal_id": signal_id,
            "projection_config_hash": projection_config_hash,
            "object_role": object_role,
            "chart_instance_id": chart_instance_id,
        },
        domain="PROJECTION",
    )


class IdentityLedger:
    """Detect conflicting payloads assigned to the same canonical ID."""

    def __init__(self) -> None:
        self._payload_hash_by_id: dict[str, str] = {}

    def register(self, envelope: IdentityEnvelope) -> str:
        existing = self._payload_hash_by_id.get(envelope.compact_id)
        if existing is None:
            self._payload_hash_by_id[envelope.compact_id] = envelope.payload_hash
            return "REGISTERED"
        if existing == envelope.payload_hash:
            return "DUPLICATE"
        raise FPI02Error(
            "FP_RC_IDENTITY_CONFLICT",
            "canonical ID maps to conflicting payload",
            {"compact_id": envelope.compact_id, "existing_payload_hash": existing, "incoming_payload_hash": envelope.payload_hash},
        )

    def snapshot_hash(self) -> str:
        return canonical_sha256(self._payload_hash_by_id)

    def size(self) -> int:
        return len(self._payload_hash_by_id)
