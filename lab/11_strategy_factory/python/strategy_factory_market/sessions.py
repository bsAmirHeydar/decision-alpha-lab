from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from .enums import TimezoneKind
from .time_kernel import TimeKernel, _ensure_utc

@dataclass(frozen=True, slots=True)
class SessionDefinition:
    session_id: str
    enabled: bool
    timezone_kind: TimezoneKind
    fixed_offset_minutes: int
    start_minute_of_day: int
    end_minute_of_day: int
    weekday_mask: int = 0b1111111

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session id required")
        if not 0 <= self.start_minute_of_day < 1440:
            raise ValueError("invalid session start")
        if not 0 <= self.end_minute_of_day < 1440:
            raise ValueError("invalid session end")
        if not 0 <= self.weekday_mask <= 127:
            raise ValueError("invalid weekday mask")

@dataclass(frozen=True, slots=True)
class SessionMatch:
    matched: bool
    session_id: str = ""
    local_minute_of_day: int = -1
    local_weekday: int = -1
    utc_offset_minutes: int = 0

class SessionSchedule:
    def __init__(self) -> None:
        self._sessions: list[SessionDefinition] = []

    def add(self, definition: SessionDefinition) -> None:
        if any(item.session_id == definition.session_id for item in self._sessions):
            raise ValueError(f"duplicate session id: {definition.session_id}")
        self._sessions.append(definition)

    @staticmethod
    def _contains(definition: SessionDefinition, minute: int) -> bool:
        start, end = definition.start_minute_of_day, definition.end_minute_of_day
        if start == end:
            return True
        if start < end:
            return start <= minute < end
        return minute >= start or minute < end

    def match(self, value: datetime, kernel: TimeKernel) -> SessionMatch:
        utc = _ensure_utc(value)
        for definition in self._sessions:
            if not definition.enabled:
                continue
            offset = kernel.resolve_offset_minutes(
                definition.timezone_kind, utc, definition.fixed_offset_minutes
            )
            local = kernel.local_datetime(
                utc, definition.timezone_kind, definition.fixed_offset_minutes
            )
            # Python Monday=0; convert to MQL Sunday=0.
            mql_weekday = (local.weekday() + 1) % 7
            if not (definition.weekday_mask & (1 << mql_weekday)):
                continue
            minute = local.hour * 60 + local.minute
            if self._contains(definition, minute):
                return SessionMatch(True, definition.session_id, minute, mql_weekday, offset)
        return SessionMatch(False)
