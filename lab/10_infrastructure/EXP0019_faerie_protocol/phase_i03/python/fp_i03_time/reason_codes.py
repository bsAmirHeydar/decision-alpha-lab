"""Closed FP-I03 reason-code registry."""
from __future__ import annotations
from dataclasses import dataclass
from fp_i02_kernel.canonical import canonical_sha256
from .errors import FPI03Error


@dataclass(frozen=True, slots=True)
class TimeReason:
    code: str
    severity: str
    meaning: str
    blocking: bool


_ROWS = (
    ("FP_TRC_READY", "INFO", "Time/calendar kernel ready", False),
    ("FP_TRC_SESSION_A", "INFO", "Reference belongs to A session", False),
    ("FP_TRC_SESSION_L", "INFO", "Reference belongs to L session", False),
    ("FP_TRC_SESSION_N", "INFO", "Reference belongs to N session", False),
    ("FP_TRC_DAILY_GAP", "INFO", "Reference belongs to 17:00-18:00 NY daily gap", True),
    ("FP_TRC_WEEKEND_CLOSED", "INFO", "Reference is outside Sunday 18:00-Friday 17:00 NY week", True),
    ("FP_TRC_LOCAL_UNIQUE", "INFO", "New York civil time maps to one UTC instant", False),
    ("FP_TRC_LOCAL_AMBIGUOUS_EARLIEST", "WARNING", "Repeated local time resolved to earliest UTC", False),
    ("FP_TRC_LOCAL_AMBIGUOUS_LATEST", "WARNING", "Repeated local time resolved to latest UTC", False),
    ("FP_TRC_LOCAL_AMBIGUOUS_REJECTED", "ERROR", "Repeated local time rejected", True),
    ("FP_TRC_LOCAL_NONEXISTENT", "ERROR", "Spring-forward local time does not exist", True),
    ("FP_TRC_YEAR_UNSUPPORTED", "ERROR", "Timestamp outside deterministic rule range", True),
    ("FP_TRC_BROKER_OFFSET_INVALID", "ERROR", "Explicit broker UTC offset invalid", True),
    ("FP_TRC_SESSION_OWNERSHIP_MISMATCH", "CRITICAL", "Session classification and interval disagree", True),
    ("FP_TRC_BOUNDARY_UNRESOLVED", "CRITICAL", "Calendar boundary could not resolve", True),
)


class TimeReasonRegistry:
    def __init__(self) -> None:
        items = tuple(TimeReason(*row) for row in _ROWS)
        if len({item.code for item in items}) != len(items):
            raise FPI03Error("FP_TRC_REASON_DUPLICATE", "duplicate time reason")
        self._items = {item.code: item for item in items}
        self.registry_hash = canonical_sha256(items)

    def resolve(self, code: str) -> TimeReason:
        try:
            return self._items[code]
        except KeyError as exc:
            raise FPI03Error("FP_TRC_REASON_UNKNOWN", f"unknown time reason {code}") from exc

    def all(self):
        return tuple(self._items[key] for key in sorted(self._items))


DEFAULT_TIME_REASON_REGISTRY = TimeReasonRegistry()
