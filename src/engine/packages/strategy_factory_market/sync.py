from __future__ import annotations

from dataclasses import dataclass
from .cache import BarCache
from .enums import SyncStatus

@dataclass(frozen=True, slots=True)
class SyncRequirement:
    symbol: str
    timeframe_seconds: int
    max_close_skew_milliseconds: int
    max_staleness_milliseconds: int

    def __post_init__(self) -> None:
        if self.timeframe_seconds <= 0:
            raise ValueError("invalid timeframe")
        if self.max_close_skew_milliseconds < 0 or self.max_staleness_milliseconds < 0:
            raise ValueError("negative synchronization tolerance")

@dataclass(frozen=True, slots=True)
class SyncResult:
    status: SyncStatus
    minimum_close_utc_milliseconds: int = 0
    maximum_close_utc_milliseconds: int = 0
    close_skew_milliseconds: int = 0
    ready_count: int = 0
    required_count: int = 0
    detail: str = ""

    @property
    def ready(self) -> bool:
        return self.status is SyncStatus.READY

class MultiSymbolSynchronizer:
    def evaluate(
        self,
        cache: BarCache,
        requirements: list[SyncRequirement],
        now_utc_milliseconds: int,
    ) -> SyncResult:
        if not requirements:
            return SyncResult(SyncStatus.MISSING_SERIES, detail="no requirements")
        close_times: list[int] = []
        for requirement in requirements:
            try:
                series = cache.get(requirement.symbol, requirement.timeframe_seconds)
                bar = series.latest
            except KeyError:
                return SyncResult(
                    SyncStatus.MISSING_SERIES,
                    ready_count=len(close_times),
                    required_count=len(requirements),
                    detail=f"missing {requirement.symbol}/{requirement.timeframe_seconds}",
                )
            if series.has_gap:
                return SyncResult(
                    SyncStatus.GAP_DETECTED,
                    ready_count=len(close_times),
                    required_count=len(requirements),
                    detail=f"gap {requirement.symbol}/{requirement.timeframe_seconds}",
                )
            close = bar.close_time.utc_epoch_milliseconds
            if now_utc_milliseconds - close > requirement.max_staleness_milliseconds:
                return SyncResult(
                    SyncStatus.STALE_SERIES,
                    ready_count=len(close_times),
                    required_count=len(requirements),
                    detail=f"stale {requirement.symbol}/{requirement.timeframe_seconds}",
                )
            close_times.append(close)
        minimum, maximum = min(close_times), max(close_times)
        skew = maximum - minimum
        allowed_skew = min(item.max_close_skew_milliseconds for item in requirements)
        status = SyncStatus.READY if skew <= allowed_skew else SyncStatus.SKEW_EXCEEDED
        return SyncResult(
            status, minimum, maximum, skew, len(close_times), len(requirements),
            "" if status is SyncStatus.READY else "close skew exceeded",
        )
