"""Research mirror of the MQL5-first Strategy Factory market services.

This package never owns live market truth. It exists for conformance tests,
offline replay, audit, and deterministic research tooling.
"""
from .enums import (
    ClockMode, DataQuality, MissingBarPolicy, SyncStatus, TimezoneKind,
)
from .time_kernel import ClockConfig, TimeKernel
from .sessions import SessionDefinition, SessionMatch, SessionSchedule
from .cache import BarCache, BarSeries, TickCache, TickSnapshot
from .sync import SyncRequirement, SyncResult, MultiSymbolSynchronizer
from .specs import SymbolSpecSnapshot, SymbolSpecCache
from .telemetry import MarketTelemetry, MarketTelemetrySnapshot

__all__ = [
    "ClockMode", "DataQuality", "MissingBarPolicy", "SyncStatus", "TimezoneKind",
    "ClockConfig", "TimeKernel", "SessionDefinition", "SessionMatch",
    "SessionSchedule", "BarCache", "BarSeries", "TickCache", "TickSnapshot",
    "SyncRequirement", "SyncResult", "MultiSymbolSynchronizer",
    "SymbolSpecSnapshot", "SymbolSpecCache", "MarketTelemetry",
    "MarketTelemetrySnapshot",
]
