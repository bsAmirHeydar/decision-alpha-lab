from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from .enums import TimestampPrecision
from .validation import require, validate_safe_identifier

@dataclass(frozen=True, slots=True, order=True)
class MarketTimestamp:
    utc_epoch_milliseconds: int
    source_timezone_id: str = "UTC"
    source_utc_offset_minutes: int = 0
    source_clock_id: str = "terminal"
    precision: TimestampPrecision = TimestampPrecision.SECONDS

    def __post_init__(self) -> None:
        require(self.utc_epoch_milliseconds >= 0, "negative UTC epoch milliseconds")
        validate_safe_identifier(self.source_timezone_id, "source_timezone_id", 96)
        validate_safe_identifier(self.source_clock_id, "source_clock_id", 96)
        require(-14 * 60 <= self.source_utc_offset_minutes <= 14 * 60, "UTC offset out of range")

    @classmethod
    def from_datetime(cls, value: datetime, *, source_timezone_id: str = "UTC",
                      source_utc_offset_minutes: int = 0, source_clock_id: str = "python",
                      precision: TimestampPrecision = TimestampPrecision.MILLISECONDS) -> "MarketTimestamp":
        require(value.tzinfo is not None, "datetime must be timezone-aware")
        epoch_ms = int(value.astimezone(timezone.utc).timestamp() * 1000)
        return cls(epoch_ms, source_timezone_id, source_utc_offset_minutes, source_clock_id, precision)

    @property
    def canonical(self) -> str:
        return "|".join([
            str(self.utc_epoch_milliseconds), self.source_timezone_id,
            str(self.source_utc_offset_minutes), self.source_clock_id, str(int(self.precision)),
        ])
