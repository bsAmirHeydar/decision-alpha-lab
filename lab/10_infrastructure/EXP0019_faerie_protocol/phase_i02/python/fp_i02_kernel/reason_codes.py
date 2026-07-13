"""Closed reason-code registry used by all later Faerie Protocol phases."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import canonical_sha256, require_semver
from .enums import ReasonCategory, Severity
from .errors import FPI02Error


@dataclass(frozen=True, slots=True)
class ReasonDescriptor:
    code: str
    category: ReasonCategory
    severity: Severity
    meaning: str
    default_visual_treatment: str
    terminal: bool = False
    execution_blocking: bool = False

    def __post_init__(self) -> None:
        if not self.code.startswith("FP_RC_"):
            raise FPI02Error("FP_RC_INVALID_REASON_CODE", "reason code must start FP_RC_")
        if not self.meaning.strip() or not self.default_visual_treatment.strip():
            raise FPI02Error("FP_RC_INVALID_REASON_DESCRIPTOR", "reason meaning/style required")


_SOURCE = (
    ("FP_RC_CONFIRMED_ACTIVE", ReasonCategory.NORMAL, Severity.INFO, "Normal confirmed signal", "solid/high opacity", False, False),
    ("FP_RC_SUPPRESSED_BY_WW", ReasonCategory.SUPPRESSION, Severity.WARNING, "Direction conflicts with active WW", "dashed/medium opacity", False, True),
    ("FP_RC_SUPPRESSED_BY_QUOTA", ReasonCategory.SUPPRESSION, Severity.WARNING, "Another earlier signal owns pair-session quota", "dotted/medium opacity", False, True),
    ("FP_RC_WW_NONE_ALLOW_BOTH", ReasonCategory.NORMAL, Severity.INFO, "No active WW with complete data", "normal plus context badge", False, False),
    ("FP_RC_WW_DATA_INCOMPLETE", ReasonCategory.DATA, Severity.ERROR, "Weekly data insufficient", "warning/low opacity", False, True),
    ("FP_RC_WW_NEUTRALIZED", ReasonCategory.LIFECYCLE, Severity.INFO, "Second symbol touched corresponding weekly side", "muted neutral", True, True),
    ("FP_RC_CONFIRMATION_DEADLINE_MISSED", ReasonCategory.LIFECYCLE, Severity.WARNING, "Confirmation candle closed outside owning session", "expired style", True, True),
    ("FP_RC_SYMMETRIC_SAME_M1", ReasonCategory.LIFECYCLE, Severity.INFO, "Both symbols touched in the same canonical M1", "neutral diagnostic", True, True),
    ("FP_RC_REFERENCE_INCOMPLETE", ReasonCategory.DATA, Severity.ERROR, "Source window incomplete", "warning diagnostic", False, True),
    ("FP_RC_REFERENCE_CONSUMED", ReasonCategory.LIFECYCLE, Severity.INFO, "Protected side previously touched", "muted unavailable", True, True),
    ("FP_RC_SELL_SPREAD_UNAVAILABLE", ReasonCategory.EXECUTION, Severity.ERROR, "Cannot form adjusted SELL stop", "execution warning", False, True),
    ("FP_RC_GEOMETRY_INVALID", ReasonCategory.EXECUTION, Severity.ERROR, "Broker/local stop geometry invalid", "execution warning", False, True),
    ("FP_RC_QUOTA_POLICY_UNSET", ReasonCategory.GOVERNANCE, Severity.CRITICAL, "Live execution disabled pending FP-DEC-012", "critical diagnostic", False, True),
    ("FP_RC_CANCELLED_BY_SECOND_TOUCH", ReasonCategory.LIFECYCLE, Severity.WARNING, "Protected symbol touched before confirmation", "cancelled style", True, True),
    ("FP_RC_NON_CANONICAL_PROFILE", ReasonCategory.CONFIGURATION, Severity.WARNING, "Research override active", "distinct banner/style", False, False),
)

_INTERNAL = (
    ("FP_RC_READY", ReasonCategory.NORMAL, Severity.INFO, "Kernel and contracts are ready", "none", False, False),
    ("FP_RC_INVALID_CONFIG", ReasonCategory.CONFIGURATION, Severity.ERROR, "Configuration contract is invalid", "critical diagnostic", True, True),
    ("FP_RC_UNKNOWN_ENUM", ReasonCategory.CONFIGURATION, Severity.ERROR, "Unknown closed enum value", "critical diagnostic", True, True),
    ("FP_RC_INVALID_SHA256", ReasonCategory.IDENTITY, Severity.ERROR, "Invalid SHA-256 field", "critical diagnostic", True, True),
    ("FP_RC_INVALID_SEMVER", ReasonCategory.CONFIGURATION, Severity.ERROR, "Invalid semantic version", "critical diagnostic", True, True),
    ("FP_RC_INVALID_IDENTIFIER", ReasonCategory.IDENTITY, Severity.ERROR, "Invalid canonical identifier", "critical diagnostic", True, True),
    ("FP_RC_NONFINITE_NUMBER", ReasonCategory.DATA, Severity.ERROR, "NaN or infinity is forbidden", "critical diagnostic", True, True),
    ("FP_RC_IDENTITY_CONFLICT", ReasonCategory.IDENTITY, Severity.CRITICAL, "Same ID maps to conflicting payload", "critical diagnostic", True, True),
    ("FP_RC_ILLEGAL_TRANSITION", ReasonCategory.LIFECYCLE, Severity.ERROR, "State transition is not permitted", "critical diagnostic", True, True),
    ("FP_RC_DUPLICATE_EVENT_DEDUPED", ReasonCategory.IDENTITY, Severity.INFO, "Exact duplicate event was deduplicated", "none", False, False),
    ("FP_RC_CHECKPOINT_VERSION_MISMATCH", ReasonCategory.DEPENDENCY, Severity.WARNING, "Checkpoint version is incompatible", "warning diagnostic", True, True),
    ("FP_RC_SOURCE_REVISION_MISMATCH", ReasonCategory.DATA, Severity.ERROR, "Source data revision differs", "warning diagnostic", True, True),
    ("FP_RC_DEPENDENCY_HASH_MISMATCH", ReasonCategory.DEPENDENCY, Severity.CRITICAL, "Pinned shared-core hash differs", "critical diagnostic", True, True),
    ("FP_RC_OPEN_DECISION_BLOCKS_LIVE", ReasonCategory.GOVERNANCE, Severity.CRITICAL, "Open owner decision blocks live authority", "critical diagnostic", False, True),
    ("FP_RC_PROJECTION_ONLY_CHANGE", ReasonCategory.NORMAL, Severity.INFO, "Projection changed without semantic identity change", "none", False, False),
    ("FP_RC_SEMANTIC_CONFIG_CHANGED", ReasonCategory.CONFIGURATION, Severity.INFO, "Behavior-bearing configuration changed", "none", False, False),
    ("FP_RC_WINDOW_INTERVAL_INVALID", ReasonCategory.DATA, Severity.ERROR, "Window interval is empty or inverted", "critical diagnostic", True, True),
    ("FP_RC_SYMBOL_PAIR_INVALID", ReasonCategory.CONFIGURATION, Severity.ERROR, "Symbol pair is invalid", "critical diagnostic", True, True),
    ("FP_RC_RELATION_DESCRIPTOR_INVALID", ReasonCategory.CONFIGURATION, Severity.ERROR, "Relation descriptor is inconsistent", "critical diagnostic", True, True),
    ("FP_RC_LIVE_AUTHORITY_FORBIDDEN", ReasonCategory.GOVERNANCE, Severity.CRITICAL, "This phase has no live authority", "critical diagnostic", True, True),
)


class ReasonRegistry:
    def __init__(self, version: str = "1.0.0", descriptors: Iterable[ReasonDescriptor] | None = None) -> None:
        self.version = require_semver(version, "reason_registry_version")
        material = tuple(descriptors or (ReasonDescriptor(*row) for row in _SOURCE + _INTERNAL))
        codes = [item.code for item in material]
        if len(codes) != len(set(codes)):
            raise FPI02Error("FP_RC_DUPLICATE_REASON_CODE", "reason registry contains duplicate code")
        self._items = {item.code: item for item in material}
        self.registry_hash = canonical_sha256({"version": self.version, "descriptors": material})

    def resolve(self, code: str) -> ReasonDescriptor:
        try:
            return self._items[code]
        except KeyError as exc:
            raise FPI02Error("FP_RC_UNKNOWN_REASON_CODE", f"unknown reason code: {code}") from exc

    def all(self) -> tuple[ReasonDescriptor, ...]:
        return tuple(self._items[key] for key in sorted(self._items))

    def contains(self, code: str) -> bool:
        return code in self._items


DEFAULT_REASON_REGISTRY = ReasonRegistry()
